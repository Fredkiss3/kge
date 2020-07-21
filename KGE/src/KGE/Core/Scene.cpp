#include "headers.h"
#include "Scene.h"
#include "KGE/Engine.h"
#include "Components.h"

namespace KGE
{

Scene::~Scene()
{
    K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before adding an entity");
    m_Pool.deadEntities.clear();
    m_Pool.inactiveEntities.clear();
    m_Pool.activeEntities.clear();
    m_Pool.currentEntities.clear();
    K_CORE_ERROR("Deleting the scene {}", GetName());
}

void Scene::add(Entity &e, EntityData *data)
{
    K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before adding an entity");

    // Construct components, then add entity to the scene
    for (auto cp : data->GetComponents())
    {
        e.addComponent(cp);
    }

    add(e);
}

void Scene::add(Entity &e)
{
    K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before adding an entity");

    ++m_lastID;
    e.scene = Ref<Scene>(this);
    e.m_ID = m_lastID;

    Ref<Entity> ref(&e);

    if (e.IsAlive())
    {
        m_Pool.activeEntities.push_back(ref);
        EventQueue::Dispatch(new EnableEntity(e));
    }
    else
    {
        m_Pool.inactiveEntities.push_back(ref);
    }
}

void Scene::Load(int index)
{
    K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before loading a new scene");
    Engine::GetInstance()->StartScene(index);
}

void Scene::Load(const char *name)
{
    K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before loading a new scene");
    Engine::GetInstance()->StartScene(name);
}

void Scene::Pop()
{
    K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before loading a new scene");
    Engine::GetInstance()->PopScene();
}

void Scene::Disable(Entity &e)
{
    if (e.scene != nullptr)
    {
        auto &active = m_Pool.activeEntities;
        auto &inactive = m_Pool.inactiveEntities;
        const auto &it = std::find(active.begin(), active.end(), Ref<Entity>(&e));

        if (it != active.end())
        {
            inactive.push_back(*it);
            active.erase(it);
            EventQueue::Dispatch(new DisableEntity(e));
        }
    }
}

void Scene::Enable(Entity &e)
{
    if (e.scene != nullptr)
    {
        auto &active = m_Pool.activeEntities;
        auto &inactive = m_Pool.inactiveEntities;
        const auto &it = std::find(inactive.begin(), inactive.end(), Ref<Entity>(&e));

        if (it != inactive.end())
        {
            active.push_back(*it);
            inactive.erase(it);
            EventQueue::Dispatch(new EnableEntity(e));
        }
    }
}

void Scene::remove(Entity &e)
{
    Ref<Entity> ref(&e);
    if (e.IsActive())
    {
        auto &active = m_Pool.activeEntities;
        auto &dead = m_Pool.deadEntities;
        const auto &it = std::find(active.begin(), active.end(), ref);

        if (it != active.end())
        {
            dead.push_back(*it);
            active.erase(it);
            EventQueue::Dispatch(new DestroyEntity(e));
        }
    }
    else
    {
        auto &inactive = m_Pool.inactiveEntities;
        auto &dead = m_Pool.deadEntities;
        const auto &it = std::find(inactive.begin(), inactive.end(), ref);

        if (it != inactive.end())
        {
            dead.push_back(*it);
            inactive.erase(it);
            EventQueue::Dispatch(new DestroyEntity(e));
        }
    }

    // Reset ID
    e.m_ID = 0;
}

} // namespace KGE