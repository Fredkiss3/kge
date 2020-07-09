#include <headers.h>
#include <KGE/Core/EntityManager.h>
#include <KGE/Core/Events.h>
#include "Engine.h"

namespace KGE
{
    Engine *Engine::s_Instance = nullptr;

    Engine::Engine() : m_Running(false),
                       m_EntityManager(),
                       m_Queue(EventQueue::GetInstance())
    {
        // Enqueue Init Event
        m_Queue->Dispatch(new Init);
    }

    Engine::~Engine()
    {
        delete m_Queue;
        m_Queue = nullptr;
    }

    void Engine::Run()
    {
        K_CORE_WARN("Starting KGE");
        GetInstance();
        s_Instance->m_Running = true;
        s_Instance->MainLoop();
        delete s_Instance;
        K_CORE_WARN("Exiting KGE");
    }

    void Engine::ShutDown()
    {
        m_Running = false;
    }

    Engine *Engine::GetInstance()
    {
        if (s_Instance == nullptr)
        {
            s_Instance = new Engine();
        }

        return s_Instance;
    }

    void Engine::DispatchEvents()
    {
        // Swap Events
        m_Queue->SwapEvents();
        while (auto e = m_Queue->GetNextEvent())
        {
            auto listeners = Get(e->GetType());
            for (auto listener : listeners)
            {
                if (!e->handled)
                {
                    K_CORE_TRACE("Calling Listener {0} for {1}", listener->GetTypeName(), e->Print());
                    listener->OnEvent(*e);
                }
            }

            // EntityManager should always handle the event
            m_EntityManager.OnEvent(*e);

            // ShutDown the engine, if we should Quit
            if (e->GetType() == EVENT_TYPE(Quit))
            {
                ShutDown();
            }
        }
    }

    void Engine::MainLoop()
    {
        while (m_Running)
        {
            K_CORE_WARN("BEGIN FRAME");
            DispatchEvents();
            K_CORE_WARN("END FRAME");
        }
    }

    void Engine::LoadScene(std::string name)
    {
        // TODO
    }

    void Engine::LoadScene(int index)
    {
        // TODO
    }

    //    void KGE::RegisterScene(Scene *scene) {
    ////        m_NextScene = scene;
    //    }
} // namespace KGE