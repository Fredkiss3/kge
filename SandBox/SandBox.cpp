#include <KGE.h>

using namespace KGE;
void setup2(Scene *scene)
{
	EventQueue::Dispatch(new Quit);
}


class MyScript : public Behaviour
{
public:
	void OnUpdate(double ts) override
	{
		++i;
	}

	int i = 0;

	CLASS_TYPE(MyScript);
};


class StopWatch : public Behaviour
{
public:
	void OnUpdate(double ts) override
	{
		m_TimeElapsed += ts;
		++m_Iterations;

		// Close after 5 seconds
		if (m_TimeElapsed >= 5)
		{
			auto avg = m_TimeElapsed / m_Iterations;
			K_CORE_DEBUG("Took an average of {} ms to iterate => {} FPS", avg * 1e3, 1.f / avg);
			K_CORE_DEBUG("With {} s passed and {} iterations", m_TimeElapsed, m_Iterations);

			auto script = GetBehaviour(MyScript::GetStaticType());
			auto tptr = GetComponent(ComponentCategory::Transform);

			K_CORE_TRACE("Has Custom Script ? {} ", HasBehaviour(MyScript::GetStaticType()) ? "true" : "false");
			K_CORE_TRACE("Has None ? {} ", HasComponent(ComponentCategory::None) ? "true" : "false");
			K_CORE_TRACE("Has Transform ? {} ", HasComponent(ComponentCategory::Transform) ? "true" : "false");

			if (script) {
				K_INFO("Got Custom Script => {}", script->GetType());
			}

			if (tptr) {
				auto transform = (TransformComponent*)tptr;
				K_INFO("Got Transform => ({}, {})", transform->pos.x, transform->pos.y);
			}

			K_INFO("Current Transform => ({}, {})", entity->GetXF().pos.x, entity->GetXF().pos.y);

			Scene::Load(1);
		}
	}

	void OnEvent(Event &e) override
	{
		K_INFO("I am catching this event: {}", e.Print());
		//EventQueue::Dispatch(new Quit);
	}

	CLASS_TYPE(StopWatch);

private:
	double m_Iterations = 0;
	double m_TimeElapsed = 0;
};

class Prefab : public EntityData
{
public:
	const char* GetName() const override 
	{
		return "Other";
	}

	const TransformComponent GetXf() const override
	{
		return TransformComponent({ 5.0f , 6.5f });
	}

	const char* GetTag() const override
	{
		return "timer";
	}

	const std::vector<Component*> GetComponents() const override
	{
		return {
			new StopWatch,
			//new MyScript,
		};
	}
};

class Prefab2 : public EntityData
{
	using  Vec2 = TransformComponent::Vec2;
private:
	std::string m_Name;
	Vec2 pos;
public:
	Prefab2(const std::string &name, Vec2 v)
		: m_Name(name), pos(v)
	{
	}

	const std::vector<Component*> GetComponents() const override
	{
		return {
			new MyScript
		};
	}

	const TransformComponent GetXf() const override
	{
		return TransformComponent(pos);
	}


	const char* GetName() const override
	{
		return m_Name.c_str();
	}

	const char* GetTag() const override
	{
		return "player";
	}
};

void setup(Scene *scene)
{
	for (int i(0); i < 5000; ++i)
	{
		auto e = Prefab2("player-" + std::to_string(i), { (double)i, (double)i });
		scene->Create(e);
	}
	K_TRACE("Added 5000 entities to {}", scene->GetName());

	auto &e = scene->Create(Prefab());

	if (scene->Reg().has<TransformComponent>(e.GetID()))
	{
		auto &t = scene->Reg().get<TransformComponent>(e.GetID());
		K_TRACE("Entity {} has a transform ! ({}, {})", e.GetName(), t.pos.x, t.pos.y);
	}
	else
	{
		K_TRACE("Entity {} has a transform !", e.GetName());
	}
	//EventQueue::Dispatch(new Quit);
}

/**
 * class Player: Entity {
 *      public:
 *      void OnUpdate(UpdateEvent& e, std::function& _) {
 *          MyScene scene2;
 *          Scene::load(scene2);
 *      }
 * }
 * */
int main()
{
	// Code for starting the logging system
	Logger::Init();
	Logger::SetLogLevel(LogLevel::TRACE);
	//setupFn fp = setup;

	//fp(0);
	//fp(1);

	// Start the engine
	auto e = Engine::GetInstance();
	auto func = [&](Scene* scene)
	{
		Scene::Load(2);
	};
	e->RegisterScene(setup, "level 1");
	e->RegisterScene(func, "level 0");
	e->RegisterScene(setup2, "level 2");
	e->Run();
	//std::cin.get();

	//InitList({});
	//InitList({ "hello", "world", "margarita", "coconut" });
	//InitList({ "50", "Cent", "Is", "A", "Bitch" });
	return 0;
}