#include "headers.h"
#include "Scene.h"
#include "KGE/Engine.h"
#include "Components.h"

namespace KGE {

    Scene::~Scene()
    {
        K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before adding an entity");
        m_Pool.deadEntities.clear();
        m_Pool.inactiveEntities.clear();
        m_Pool.activeEntities.clear();
        m_Pool.currentEntities.clear();
        K_CORE_ERROR("Deleting the scene {}", GetName());
    }

    void Scene::add(Entity& e, EntityData* data) {
        K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before adding an entity");

        // Construct components, then add entity to the scene
        for (auto cp : data->GetComponents()) {
            e.addComponent(cp);
        }

        add(e);
    }


    void Scene::add(Entity& e)
    {
        K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before adding an entity");

        ++m_lastID;
        e.scene = Ref<Scene>(this);
        e.m_ID = m_lastID;

        if (e.IsAlive()) {
            m_Pool.activeEntities.push_back(e);
        }
        else {
            m_Pool.inactiveEntities.push_back(e);
        }
    }

    void Scene::Load(int index)
    {
        K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before loading a new scene");
        Engine::GetInstance()->StartScene(index);
    }

    void Scene::Load(const char* name)
    {
        K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before loading a new scene");
        Engine::GetInstance()->StartScene(name);
    }

    void Scene::Pop()
    {
        K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before loading a new scene");
        Engine::GetInstance()->PopScene();
    }

} // namespace KGE