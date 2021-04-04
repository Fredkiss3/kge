#include <headers.h>
#include <KGE/Core/ComponentManager.h>
#include <KGE/Events/Events.h>
#include <KGE/Graphics/Events.h>
#include "Engine.h"
#include "KGE/Core/Scene.h"

namespace KGE
{
	Ref<Engine> Engine::s_Instance = nullptr;

	Engine::Engine(const WindowProps& props, bool Debug)
		: m_DebugMode(Debug),
		m_Running(false),
		m_Queue(EventQueue::GetInstance()),
		m_CurScene(nullptr),
		m_CurrentSceneIndex(-1),
		m_NextSceneIndex(0),
		m_Renderer(props),
		m_Clock(Clock::now())
	{
		m_Queue->Dispatch(new WindowResize{(int)props.Width, (int)props.Height});
		// Add Debug Manager only if engine should be run on Debug Mode
		if (m_DebugMode) {
			m_Managers.push_back(&m_DebugManager);
		}

		m_Managers.push_back(&m_Renderer);
		m_Managers.push_back(&m_ScriptManager);
		m_Managers.push_back(&m_PhysicsManager);

	}

	Engine::~Engine()
	{
		// teardown the current scene
		if (m_CurScene)
		{
			if (m_CurScene->m_Started)
			{
				m_CurScene->tearDown();
			}
		}
	}

	void Engine::Run()
	{
		K_CORE_WARN("Starting KGE");
		s_Instance->m_Running = true;
		s_Instance->Init();
		s_Instance->MainLoop();
		K_CORE_WARN("Exiting KGE");
	}

	void Engine::ShutDown()
	{
		m_Running = false;
	}

	const Ref<Engine>& Engine::GetInstance(const WindowProps& props, bool Debug)
	{
		if (s_Instance == nullptr)
		{
			s_Instance = Ref<Engine>(new Engine(props, Debug));
		}

		return s_Instance;
	}

	void Engine::LoadScene(int index)
	{
		if (index < m_ScenesData.size() && index >= 0)
		{
			m_NextSceneIndex = index;
		}
		else
		{
			K_CORE_ERROR("The scene at index {} is not registered", index);
		}
	}

	void Engine::LoadScene(const char* name)
	{
		bool found = false;
		for (int i(0); i < m_ScenesData.size(); ++i)
		{
			auto& data = m_ScenesData[i];

			if (data.name == name)
			{
				found = true;
				m_NextSceneIndex = i;
				break;
			}
		}

		if (!found)
		{
			K_CORE_ERROR("The scene named '{}' is not registered", name);
		}
	}

	void Engine::PopScene()
	{
		m_NextSceneIndex--;
		if (m_NextSceneIndex < 0)
		{
			m_Queue->Dispatch(new Quit);
		}
		//else
		//{
		//	//LoadScene(m_CurrentSceneIndex);
		//}
	}

	void Engine::RegisterScene(SetupFn fn, const char* name)
	{
		bool found = false;
		for (size_t i(0); i < m_ScenesData.size(); ++i)
		{
			auto& data = m_ScenesData[i];
			if (data.name == name)
			{
				found = true;
				K_CORE_ERROR("There cannot be two scenes with the name '{}'", name);
			}
		}

		if (!found)
		{
			m_ScenesData.push_back({ fn, name });
		}
	}

	Ref<Scene>& Engine::GetCurrentScene()
	{
		return m_CurScene;
	}

	bool Engine::DispatchEvents()
	{
		// Swap Events
		m_Queue->SwapEvents();
		bool shouldUpdate = true;

		// Debug Drawing only on debug  
		while (auto e = m_Queue->GetNextEvent())
		{
			e->scene = m_CurScene;

			if (e->GetType() == EVENT_TYPE(DilateTime)) {
				timeMultiplier = (static_cast<DilateTime&>(*e)).dilation;
			}

			// All managers should handle the event
			for (auto manager : m_Managers)
			{
				if (!e->handled)
				{
					manager->OnEvent(*e);
				}
				else
				{
					break;
				}
			}

			// ShutDown the engine, if we should Quit
			if (e->GetType() == EVENT_TYPE(Quit))
			{
				shouldUpdate = false;
				ShutDown();
			}
		}

		return shouldUpdate;
	}

	void Engine::UpdateSystems()
	{
		auto now = Clock::now();

		std::chrono::duration<double> duration = (now - m_Clock);
		m_Clock = now;

		// Update scripts for each frame
		m_ScriptManager.OnUpdate(duration.count() * timeMultiplier);


		// Physics Framerate is fixed to 50 FPS
		m_Accumulated_Time += duration.count();
		if (m_Accumulated_Time >= PHYSICS_FPS) {

			// Send Fixed Update then dispatch to scripts
			m_Queue->Dispatch(new FixedUpdate{ m_Accumulated_Time });
			DispatchEvents();

			m_PhysicsManager.OnUpdate(m_Accumulated_Time);
			m_Accumulated_Time = 0.0f;
		}

		// Render Scene
		m_Renderer.OnPreRender();
		m_Renderer.OnRender();

		if (m_DebugMode) {
			m_DebugManager.Draw();
		}

		// Apply Post Render
		m_Renderer.OnPostRender();
	}

	void Engine::CheckNextScene()
	{
		if (m_NextSceneIndex != m_CurrentSceneIndex && m_ScenesData.size() > 0) {
			m_CurrentSceneIndex = m_NextSceneIndex;

			// Dispatch the event to managers before doing anything
			if (m_CurScene != nullptr) {
				DispatchEvents();
			}

			StartScene(m_NextSceneIndex);
		}
	}

	void Engine::StartScene(int index)
	{
		// Tear down any current scene
		if (m_CurScene)
		{
			m_CurScene->tearDown();
		}

		// Then register a new scene and setup the new scene
		auto& data = m_ScenesData[index];
		m_CurScene = CreateRef<Scene>(data.fn, data.name);
		m_CurScene->setUp();
	}

	void Engine::Init()
	{
		m_Renderer.OnInit();
		if (m_DebugMode) {
			m_DebugManager.OnInit();
		}
	}

	void Engine::PreUpdate()
	{
		CheckNextScene();
	}

	void Engine::MainLoop()
	{
		// Setup the first scene
		while (m_Running)
		{
			//K_CORE_WARN("BEGIN FRAME");
			PreUpdate();
			if (DispatchEvents())
			{
				UpdateSystems();
			}
			//K_CORE_WARN("END FRAME");
		}
	}
} // namespace KGE