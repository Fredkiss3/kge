#pragma once

#include "headers.h"
#include "Base.h"
#include "Utils/Log.h"
#include "Core/ComponentManager.h"
#include "Events/Event.h"
#include <KGE/Core/Scene.h>
#include "KGE/Core/ScriptManager.h"

/*
 * The Engine class is a singleton that launches the game
 * */
namespace KGE
{
typedef void (*SetupFn)(Scene *);
typedef std::chrono::high_resolution_clock Clock;

struct SceneData
{
    SetupFn fn;
    std::string name;
};

//class Scene;

class Engine : public ListenerContainer
{
public:
    ~Engine();

    void Run();

    void ShutDown();

    //static Ref<Engine> GetInstance(void(*fn)(Scene*));

    //void StartScene(void(*fn)(Scene*));
    void StartScene(int index);
    void StartScene(const char *name);
    void PopScene();
    void RegisterScene(SetupFn, const char *name = "new Scene");
    //void StartScene(void(*fn)(Scene*));

    Ref<Scene> &GetCurrentScene();

public:
    static const Ref<Engine> &GetInstance();

    static const Ref<Engine> &GetStaticInstance()
    {
        return s_Instance;
    }

private:
    Engine();

    //void SetupScene();
    void MainLoop();
    bool DispatchEvents();
    void UpdateSystems();

private:
    bool m_Running;
    int m_CurrentSceneIndex;

    ScriptManager m_ScriptManager;

    std::vector<ComponentManager *> m_Managers;

    Ref<EventQueue> m_Queue;

    static Ref<Engine> s_Instance;

    Ref<Scene> m_CurScene;

    std::vector<SceneData> m_ScenesData;

    // the clock we will be using
    std::chrono::time_point<std::chrono::system_clock> m_Clock;
};

} // namespace KGE