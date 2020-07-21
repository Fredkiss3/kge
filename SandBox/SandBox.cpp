#include <KGE.h>

using namespace KGE;
void setup2(Scene *scene)
{
	K_TRACE("Setting Up a new Scene {}", scene->GetName());
	EventQueue::Dispatch(new Quit);
}

class Timer : public Behaviour
{
public:
	void OnUpdate(double ts) override
	{
		m_TimeElapsed += ts;
		++m_Iterations;

		//K_INFO( m_TimeElapsed, ts * 1000.f, (1.f/ts));
		//std::cout << m_TimeElapsed << " sec passed with timestep of " << ts * 1000.f << " ms (" << (1.f / ts) << " FPS)\n";
		// Close after 5 seconds
		if (m_TimeElapsed >= 5)
		{
			auto avg = m_TimeElapsed / m_Iterations;
			K_CORE_DEBUG("Took an average of {} ms to iterate => {} FPS", avg * 1e3, 1.f / avg);
			K_CORE_DEBUG("With {} s passed and {} iterations", m_TimeElapsed, m_Iterations);
			Scene::Load(1);
		}
	}

	void OnEvent(Event const &e) override
	{
		K_INFO("I am catching this event: {}", e.Print());
		//EventQueue::Dispatch(new Quit);
	}

	CLASS_TYPE(Timer);

private:
	double m_Iterations = 0;
	double m_TimeElapsed = 0;
};

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

class Prefab : public EntityData
{
	std::vector<Component *> GetComponents() const override
	{
		return {
			new Transform({10.0f, 10.0f}, {1, 1}, 0),
			new Timer,
		};
	};
};

class Prefab2 : public EntityData
{
	std::vector<Component *> GetComponents() const override
	{
		return {
			new Transform({5.0f, 5.0f}, {2, 2}, 0),
			new MyScript,
		};
	};
};

void setup(Scene *scene)
{
	K_TRACE("Setting Up {}", scene->GetName());

	for (int i(0); i < 5000; ++i)
	{
		Entity e(std::string("player") + std::to_string(i));

		scene->add(e, new Prefab2);
	}
	K_TRACE("Added 5000 entities to {}", scene->GetName());

	Entity e("other");

	scene->add(e, new Prefab);

	if (e.hasComponent(ComponentCategory::Transform))
	{
		auto &t = castRef<Transform>(e.GetComponent(ComponentCategory::Transform));
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
	e->RegisterScene(setup, "level 1");
	e->RegisterScene(setup2, "level 2");
	e->Run();
	std::cin.get();

	//InitList({});
	//InitList({ "hello", "world", "margarita", "coconut" });
	//InitList({ "50", "Cent", "Is", "A", "Bitch" });
	return 0;
}