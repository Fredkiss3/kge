//#define _CRT_SECURE_NO_WARNINGS
//#define GLFW_INCLUDE_NONE
#include <KGE.h>

using namespace KGE;
void setup2(Scene* scene)
{
	EventQueue::Dispatch(new Quit);
}

class MyScript : public Behaviour
{
public:
	MyScript()
	{
		Bind<WindowResize>(K_BIND_EVENT_FN(MyScript::OnWindowResize));
		Bind<KeyReleased>(K_BIND_EVENT_FN(MyScript::OnKeyReleased));
		Bind<MouseReleased>(K_BIND_EVENT_FN(MyScript::OnMouseReleased));
		Bind<MouseScrolled>(K_BIND_EVENT_FN(MyScript::OnMouseScrolled));
		Bind<ImGuiDraw>(K_BIND_EVENT_FN(MyScript::OnDebug));
		//Bind<KeyPressed>(K_BIND_EVENT_FN(MyScript::OnKeyPressed));
		//Bind<MousePressed>(K_BIND_EVENT_FN(MyScript::OnMousePressed));
		//Bind<MouseMoved>(K_BIND_EVENT_FN(MyScript::OnMouseMoved));
	}

	void OnUpdate(double ts) override
	{
		auto& transform = entity->xf();
		/*K_INFO("Got Transform => position : {} || rotation : {} || scale : {}",
			transform.pos,
			transform.rotation,
			transform.scale);
		K_TRACE("Mouse Position : {}, {}", Input::GetMousePos().x, Input::GetMousePos().y);
*/

		if (Input::IsKeyPressed(Key::Space))
		{
			K_TRACE("Key Space Pressed !");
		}

		if (Input::IsMousePressed(Mouse::ButtonLeft))
		{
			K_TRACE("Mouse Primary Pressed !");
		}
	}

	void OnWindowResize(WindowResize& ev)
	{
		K_INFO("Window has been resized to : {} px, {} px", ev.width, ev.height);
	}

	void OnKeyPressed(KeyPressed& ev)
	{
		K_INFO("Key is being pressed : {} ", (char)ev.keyCode);
	}

	void OnKeyReleased(KeyReleased& ev)
	{
		K_INFO("Key is released : {}", (char)ev.keyCode);
	}

	void OnMousePressed(MousePressed& ev)
	{
		K_INFO("Mouse is pressed : {}", ev.button);
	}

	void OnMouseReleased(MouseReleased& ev)
	{
		K_INFO("Mouse is released : {}", ev.button);
	}

	void OnMouseMoved(MouseMoved& ev)
	{
		K_INFO("mouse is moving : {}, {}", ev.pos.x, ev.pos.y);
	}

	void OnMouseScrolled(MouseScrolled& ev)
	{
		K_INFO("mouse is scrolling : {}, {}", ev.offset.x, ev.offset.y);
	}

	void OnDebug(ImGuiDraw& ev)
	{
		ImGui::Begin("My Script");
		auto& color = entity->GetScene()->bgColor;
		float colors[] = { color.r, color.g, color.b, color.a };
		if (ImGui::ColorEdit4("Bg Color", colors)) {
			color = { colors[0], colors[1], colors[2], colors[3] };
		}
		ImGui::End();
	}

};

class StopWatch : public Behaviour
{
public:
	StopWatch(int endTime = 5) : m_EndTime(endTime) {};
	void OnUpdate(double ts) override
	{
		m_TimeElapsed += ts;
		++m_Iterations;

		// Close after 5 seconds
		if (m_TimeElapsed >= m_EndTime)
		{
			auto avg = m_TimeElapsed / m_Iterations;
			K_CORE_DEBUG("Took an average of {} ms to iterate => {} FPS", avg * 1e3, 1.f / avg);
			K_CORE_DEBUG("With {} s passed and {} iterations", m_TimeElapsed, m_Iterations);

			//auto script = m_Entity->GetBehaviour<MyScript>();
			auto transform = entity->GetComponent<TransformComponent>();

			K_CORE_TRACE("Has Custom Script ? {} ", entity->hasBehaviour<MyScript>() ? "true" : "false");
			K_CORE_TRACE("Has Transform ? {} ", entity->hasComponent<TransformComponent>() ? "true" : "false");

			{
				K_INFO("Got Transform => position : {} || rotation : {} || scale : {}",
					transform.pos,
					transform.rotation,
					transform.scale);
			}

			K_INFO("Current Transform => ({}, {})", entity->xf().pos.x, entity->xf().pos.y);

			Scene::Load(1);
		}
	}

public:
	double m_Iterations = 0;
	double m_TimeElapsed = 0;
	double m_EndTime;
};

class Prefab : public EntityData
{
public:
	Prefab() : EntityData("Timer", Vec2{ 5.0f, 6.5f }) {};

	Behaviour* GetScript() const override
	{
		return {
			//new MyScript
		};
	}



};

/*
* 
* import Vector, Scene from KGE;
import Update from KGE::Events;


class Player extends Sprite {
   constructor() {
     this.sprite = 'player.png';
   }

   onUpdate(event: Update) {
      this.position += Vector.Right() * event.ts;
   }
}

* 
* 
*/

class Prefab2 : public EntityData
{
public:
	Prefab2(const std::string& name, Vec2 v = { 0.0 })
		: EntityData(name, v)
	{
	}
};


struct Moveable : public Behavior
{
	KeyCode UpKey;
	KeyCode DownKey;
	KeyCode LeftKey;
	KeyCode RightKey;
	float Speed = 10.f;
	double lastTs = 0.0f;
	bool IsPerspective = false;

	Moveable(KeyCode up = KeyCode::Up,
		KeyCode down = KeyCode::Down,
		KeyCode left = KeyCode::Left,
		KeyCode right = KeyCode::Right) : UpKey(up), DownKey(down), LeftKey(left), RightKey(right) {
		Bind<ImGuiDraw>(K_BIND_EVENT_FN(Moveable::OnDebug));
	}


	void OnDebug(ImGuiDraw& ev)
	{
		ImGui::Begin(entity->tag().c_str());
		
		auto& pos = entity->xf().pos;
		auto& scale = entity->xf().scale;
		auto& rotation = entity->xf().rotation;

		ImGui::DragFloat3("Translation", &pos.x, (Speed * lastTs));
		ImGui::DragFloat3("Rotation", &rotation.x, (Speed * lastTs));
		ImGui::DragFloat3("Scale", &scale.x, (Speed * lastTs));

		if (entity->hasComponent<CameraComponent>()) {
			ImGui::Checkbox("Perspective ?", &IsPerspective);
		}

		if (entity->hasComponent<SpriteComponent>()) {
			auto& color = entity->GetComponent<SpriteComponent>().color;
			ImGui::ColorEdit4("Color", &color.r);
		}

		ImGui::End();
	}

	void OnUpdate(double ts) override
	{
		lastTs = ts;
		auto& transform = entity->xf();

		auto direction = Vec2::Zero();
		auto zoom = 0;

		if (Input::IsKeyPressed(UpKey))
		{
			direction = direction + Vec2::Up();
		}

		if (Input::IsKeyPressed(DownKey))
		{
			direction = direction + Vec2::Down();
		}
		
		if (Input::IsKeyPressed(LeftKey))
		{
			direction = direction + Vec2::Left();
		}
		
		if (Input::IsKeyPressed(RightKey))
		{
			direction = direction + Vec2::Right();
		}

		if (Input::IsKeyPressed(KeyCode::KPAdd)) {
			zoom = -1;
		}
		else if (Input::IsKeyPressed(KeyCode::KPSubtract)) {
			zoom = +1;
		}

		if (entity->hasComponent<CameraComponent>()) {
			K_TRACE("{} * {} = {} ", zoom, Vec2::Unit(), (zoom * Vec2::Unit()));
			transform.scale = transform.scale + (zoom * Vec2::Unit() * Speed * ts/2);

			auto& cc = entity->GetComponent<CameraComponent>();
			if (IsPerspective && cc.GetProjectionType() == ProjectionType::Orthographic) {
				cc.SetProjectionType(ProjectionType::Perspective);
			}
			else if (!IsPerspective && cc.GetProjectionType() == ProjectionType::Perspective) {
				cc.SetProjectionType(ProjectionType::Orthographic);
			}
		}

		transform.pos = transform.pos + (direction * Speed * ts);
		
	}
};

void setup(Scene* scene)
{
	auto& e6 = scene->Create({ "Dynamic", Vec2{1 , -1} });
	auto& e8 = scene->CreatePrefab<Prefab2>("Static", Vec2{ 0.0, 1 });

	e6.AddComponent<SpriteComponent>(Color::Blue());
	e6.AddBehavior<Moveable>();

	e8.AddComponent<SpriteComponent>("assets/textures/ChernoLogo.png");

	auto& cam = scene->GetMainCamera();
	cam.AddBehavior<Moveable>(KeyCode::W,KeyCode::S, KeyCode::Q,KeyCode::D);


	for (auto it : scene->all()) {
		auto& e = it.second;

		if (e.hasBehaviour<StopWatch>()) {
			K_TRACE("Entity {} has a 'StopWatch' of {} seconds", e.tag(), e.GetBehaviour<StopWatch>().m_EndTime);
		}

		else if (e.hasBehaviour<MyScript>()) {
			K_TRACE("Entity {} has a 'MyScript'", e.tag());
		}

		K_TRACE("Entity {} has a transform ! ({}, {})", e.tag(), e.xf().pos.x, e.xf().pos.y);
	}
}

int main()
{
	// Code for starting the logging system
	Logger::Init();
	Logger::SetLogLevel(LogLevel::TRACE);
	// Start the engine
	auto e = Engine::GetInstance({ "SandBox", 600, 600 }, true);
	auto func = [&](Scene* scene) {
		Scene::Load(2);
	};
	e->RegisterScene(setup, "level 1");
	e->RegisterScene(func, "level 0");
	e->RegisterScene(setup2, "level 2");
	e->Run();
	return 0;
}
