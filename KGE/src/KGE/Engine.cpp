#include <headers.h>
#include <KGE/Core/ComponentManager.h>
#include <KGE/Events/Events.h>
#include "Engine.h"

namespace KGE
{
	Ref<Engine> Engine::s_Instance = nullptr;

	Engine::Engine() : m_Running(false),
		m_Queue(EventQueue::GetInstance()),
		m_CurScene(nullptr),
		m_CurrentSceneIndex(0),
		m_Clock(Clock::now())
	{
		// Enqueue Init Event
		// Only for tests
		// m_Queue->Dispatch(new Init);
		m_Managers.push_back(&m_ScriptManager);
	}

	Engine::~Engine()
	{
		// teardown the current scene
		if (m_CurScene) {
			if (m_CurScene->m_Started) {
				m_CurScene->tearDown();
			}
		}
	}

	void Engine::Run()
	{
		K_CORE_WARN("Starting KGE");
		s_Instance->m_Running = true;
		s_Instance->MainLoop();
		K_CORE_WARN("Exiting KGE");
	}

	void Engine::ShutDown()
	{
		m_Running = false;
	}

	const Ref<Engine>& Engine::GetInstance()
	{
		if (s_Instance == nullptr)
		{
			s_Instance = Ref<Engine>(new Engine);
		}

		return s_Instance;
	}

	void Engine::StartScene(int index)
	{
		if (index < m_ScenesData.size()) {
			// Tear down any current scene
			if (m_CurScene) {
				m_CurScene->tearDown();
			}

			auto& data = m_ScenesData[index];

			// Then register a new scene and setup the new scene
			m_CurScene = CreateRef<Scene>(data.fn, data.name);
			m_CurScene->setUp();
		}
		else {
			K_CORE_ERROR("The scene at index {} is not registered", index);
		}
	}



	void Engine::StartScene(const char* name)
	{
		bool found = false;
		for (int i(0); i < m_ScenesData.size(); ++i) {
			auto& data = m_ScenesData[i];

			if (data.name == name) {
				found = true;
				m_CurrentSceneIndex = i;

				// Tear down any current scene
				if (m_CurScene) {
					m_CurScene->tearDown();
				}

				// Then register a new scene
				m_CurScene = CreateRef<Scene>(data.fn, data.name);
				m_CurScene->setUp();
				break;
			}
		}

		if (!found) {
			K_CORE_ERROR("The scene named '{}' is not registered", name);
		}
	}

	void Engine::PopScene()
	{
		m_CurrentSceneIndex--;
		if (m_CurrentSceneIndex < 0) {
			m_Queue->Dispatch(new Quit);
		}
		else {
			StartScene(m_CurrentSceneIndex);
		}
	}

	void Engine::RegisterScene(SetupFn fn, const char* name)
	{
		bool found = false;
		for (int i(0); i < m_ScenesData.size(); ++i) {
			auto& data = m_ScenesData[i];
			if (data.name == name) {
				found = true;
				K_CORE_ERROR("There cannot be two scenes with the name '{}'", name);
			}
		}

		if (!found) {
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
		while (auto e = m_Queue->GetNextEvent())
		{
			e->scene = m_CurScene;

			// All managers should handle the event
			for (auto manager : m_Managers)
			{
				if (!e->handled)
				{
					K_CORE_TRACE("Calling Listener {0} for {1}", manager->GetTypeName(), e->Print());
					manager->OnEvent(*e);
				}
				else {
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

	void Engine::UpdateSystems() {
		auto now = Clock::now();

		std::chrono::duration<double> duration = (now - m_Clock);
		// Update scripts
		m_ScriptManager.OnUpdate(duration.count());

		m_Clock = now;
	}

	void Engine::MainLoop()
	{
		// Setup the first scene
		StartScene(0);
		while (m_Running)
		{
			//K_CORE_WARN("BEGIN FRAME");
			if (DispatchEvents()) {
				UpdateSystems();
			}
			//K_CORE_WARN("END FRAME");
		}
	}
} // namespace KGE