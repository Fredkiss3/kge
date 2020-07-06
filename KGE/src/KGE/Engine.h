#pragma once

#include <headers.h>
#include <KGE/Core/Log.h>
#include <KGE/Base.h>
#include <KGE/Core/Event.h>
#include <KGE/Core/EntityManager.h>

/*
 * The Engine class is a singleton that launches the game
 * */
namespace KGE
{
    class Scene;

    class Engine : public ListenerContainer
    {
    public:
        ~Engine();

        static void Run();

        void ShutDown();

        static Engine *GetInstance();

        void RegisterScene(Scene *scene) {}

        //        Scene *GetCurrentScene() { return m_CurScene; }

    private:
        Engine();

        void LoadScene(int index);
        void LoadScene(std::string name);

        void MainLoop();

    private:
        bool m_Running;
        EntityManager m_EntityManager;
        EventQueue *m_Queue;
        static Engine *s_Instance;

        void DispatchEvents();
    };
} // namespace KGE