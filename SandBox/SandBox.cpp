#define _CRT_SECURE_NO_WARNINGS
#define GLFW_INCLUDE_NONE
#include <KGE.h>

using namespace KGE;
void setup2(Scene *scene)
{
	EventQueue::Dispatch(new Quit);
}

class MyScript : public Behaviour
{
public:
	MyScript()
	{
		Bind<WindowResize>(K_BIND_EVENT_FN(MyScript::OnWindowResize));
		//Bind<KeyPressed>(K_BIND_EVENT_FN(MyScript::OnKeyPressed));
		Bind<KeyReleased>(K_BIND_EVENT_FN(MyScript::OnKeyReleased));
		Bind<MouseReleased>(K_BIND_EVENT_FN(MyScript::OnMouseReleased));
		//Bind<MousePressed>(K_BIND_EVENT_FN(MyScript::OnMousePressed));
		//Bind<MouseMoved>(K_BIND_EVENT_FN(MyScript::OnMouseMoved));
		Bind<MouseScrolled>(K_BIND_EVENT_FN(MyScript::OnMouseScrolled));
	}

	void OnUpdate(double ts) override
	{
		K_TRACE("Mouse Position : {}, {}", Input::GetMousePos().x, Input::GetMousePos().y);

		if (Input::IsKeyPressed(Key::Space))
		{
			K_TRACE("Key Space Pressed !");
		}

		if (Input::IsMousePressed(Mouse::Button0))
		{
			K_TRACE("Mouse Primary Pressed !");
		}
	}

	void OnWindowResize(WindowResize &ev)
	{
		K_INFO("Window has been resized to : {} px, {} px", ev.width, ev.height);
	}

	void OnKeyPressed(KeyPressed &ev)
	{
		K_INFO("Key is being pressed : {} ", (char)ev.keyCode);
	}

	void OnKeyReleased(KeyReleased &ev)
	{
		K_INFO("Key is released : {}", (char)ev.keyCode);
	}

	void OnMousePressed(MousePressed &ev)
	{
		K_INFO("Mouse is pressed : {}", ev.button);
	}

	void OnMouseReleased(MouseReleased &ev)
	{
		K_INFO("Mouse is released : {}", ev.button);
	}

	void OnMouseMoved(MouseMoved &ev)
	{
		K_INFO("mouse is moving : {}, {}", ev.pos.x, ev.pos.y);
	}

	void OnMouseScrolled(MouseScrolled &ev)
	{
		K_INFO("mouse is scrolling : {}, {}", ev.offset.x, ev.offset.y);
	}

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

			if (script)
			{
				K_INFO("Got Custom Script => {}", script->GetType());
			}

			if (tptr)
			{
				auto transform = (TransformComponent *)tptr;
				K_INFO("Got Transform => position : {} || rotation : {} || scale : {}",
					   transform->pos,
					   transform->scale,
					   transform->rotation);
			}

			K_INFO("Current Transform => ({}, {})", entity->GetXF().pos.x, entity->GetXF().pos.y);

			Scene::Load(1);
		}
	}

	CLASS_TYPE(StopWatch);

private:
	double m_Iterations = 0;
	double m_TimeElapsed = 0;
};

class Prefab : public EntityData
{
public:
	const char *GetName() const override
	{
		return "Other";
	}

	const TransformComponent GetXf() const override
	{
		return TransformComponent(Vec2{5.0f, 6.5f});
	}

	const char *GetTag() const override
	{
		return "timer";
	}

	const std::vector<Component *> GetComponents() const override
	{
		return {
			//new StopWatch,
			new MyScript,
		};
	}
};

class Prefab2 : public EntityData
{
private:
	std::string m_Name;
	Vec2 pos;

public:
	Prefab2(const std::string &name, Vec2 v)
		: m_Name(name), pos(v)
	{
	}

	const std::vector<Component *> GetComponents() const override
	{
		return {
			new MyScript};
	}

	const TransformComponent GetXf() const override
	{
		return TransformComponent(pos);
	}

	const char *GetName() const override
	{
		return m_Name.c_str();
	}

	const char *GetTag() const override
	{
		return "player";
	}
};

void setup(Scene *scene)
{
	int n(5);
	auto prefab = Prefab();
	auto &e = scene->Create(prefab);

	//for (int i(0); i < n; ++i)
	//{
	//	auto e = Prefab2("player-" + std::to_string(i), { (double)i, (double)i });
	//	scene->Create(e);
	//}
	//K_TRACE("Added 5000 entities to {}", scene->GetName());

	//if (scene->Reg().has<TransformComponent>(e.GetID()))
	//{
	//	auto &t = scene->Reg().get<TransformComponent>(e.GetID());
	//	K_TRACE("Entity {} has a transform ! ({}, {})", e.GetName(), t.pos.x, t.pos.y);
	//}
	//else
	//{
	//	K_TRACE("Entity {} has a transform !", e.GetName());
	//}
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
	auto e = Engine::GetInstance("SandBox");
	auto func = [&](Scene *scene) {
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
