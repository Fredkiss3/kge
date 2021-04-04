#pragma once

#include "headers.h"
#include "Base.h"
#include "Utils/Log.h"
#include "Core/ComponentManager.h"
#include "Events/Event.h"
#include "KGE/Core/Scene.h"
#include "KGE/Core/ScriptManager.h"
#include "KGE/Physics/PhysicsManager.h"
#include "KGE/Graphics/Renderer.h"
#include "KGE/Graphics/DebugManager.h"

/*
 * The Engine class is a singleton that launches the game
 * */
namespace KGE
{
	typedef std::function<void(Scene*)> SetupFn;
	typedef std::chrono::high_resolution_clock Clock;

	struct SceneData
	{
		SetupFn fn;
		std::string name;
	};

	//class Scene;

	class Engine
	{
	public:
		~Engine();

		void Run();

		void ShutDown();

		//static Ref<Engine> GetInstance(void(*fn)(Scene*));

		//void StartScene(void(*fn)(Scene*));
		void LoadScene(int index);
		void LoadScene(const char* name);
		void PopScene();
		void RegisterScene(SetupFn, const char* name = "new Scene");
		//void StartScene(void(*fn)(Scene*));

		Ref<Scene>& GetCurrentScene();
		
		const std::string& GetApplicationName() { return m_ApplicationName; }

	public:
		static const Ref<Engine>& GetInstance(const WindowProps& props = {}, bool Debug = true);

		static const Ref<Engine>& GetStaticInstance()
		{
			return s_Instance;
		}

	private:
		Engine(const WindowProps& props, bool Debug=true);

		void MainLoop();
		bool DispatchEvents();
		void UpdateSystems();
		void CheckNextScene();
		void StartScene(int index);
		void Init();
		void PreUpdate();

	private:
		bool m_Running;
		bool m_DebugMode;
		int m_CurrentSceneIndex;

		// In order to defer the start of a scene
		int m_NextSceneIndex;

		// Component Managers
		ScriptManager m_ScriptManager;
		PhysicsManager m_PhysicsManager;
		DebugManager m_DebugManager;
		Renderer m_Renderer;

		std::vector<ComponentManager*> m_Managers;

		// For Physics Updating
		const double PHYSICS_FPS = 1.0f / 50.0f;
		double m_Accumulated_Time = 0.0f;

		// For Systems Update
		float timeMultiplier = 1.0f;

		// Event Queue & Scene Stuff
		Ref<EventQueue> m_Queue;
		static Ref<Engine> s_Instance;
		Ref<Scene> m_CurScene;
		std::vector<SceneData> m_ScenesData;
	private:
		//For renderer
		std::string m_ApplicationName;

		// Use different clocks depending if we are using mvsc or gcc
#ifdef __GNUG__
		std::chrono::time_point<std::chrono::system_clock> m_Clock;
#else
		std::chrono::time_point<std::chrono::steady_clock> m_Clock;
#endif
	};

} // namespace KGE