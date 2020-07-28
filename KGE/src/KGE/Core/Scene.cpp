#include "headers.h"
#include "Scene.h"
#include "KGE/Engine.h"
#include "entt/entt.hpp"

namespace KGE
{
	template<typename Cp>
	void InitC(entt::registry& reg, entt::entity e) 
	{
		auto cp = reg.try_get<Cp>(e);

		if (cp) {
			cp->Init();
		}
	}

	Scene::Scene(const SetupFn& fn, const std::string& name) 
		: m_SetupFn(fn), m_Name(name)
	{
		// Initialize on construct
		m_Registry.on_construct<ScriptComponent>().connect<&InitC<ScriptComponent>>();
	}

	Scene::~Scene()
	{
		K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before adding an entity");
		m_Registry.clear();
		m_EntityMap.clear();
		K_CORE_ERROR("Deleting the scene {}", GetName());
	}

	Entity& Scene::Create(EntityData& data)
	{
		K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before adding an entity");

		auto id = m_Registry.create();

		// Keep a reference to entity in order to not prevent it from deletion
		m_EntityMap[id] = Entity(id);
		auto& e = m_EntityMap[id];

		e.scene = this;

		// add a transform & set name and stuff
		auto& transform = m_Registry.emplace<TransformComponent>(e.m_ID, data.GetXf());
		e.m_Name = data.GetName();
		e.m_Tag = data.GetTag();
		e.transform = transform;
		e.transform.entity = &e;

		// add components to registry
		for (auto& cp : data.GetComponents())
		{
			cp->entity = &e;

			switch (cp->GetCategory())
			{
			case ComponentCategory::Behaviour:
				m_Registry.get_or_emplace<ScriptComponent>(e.m_ID)
					.Add(dynamic_cast<Behaviour&>(*cp));
				
				m_Registry.sort<ScriptComponent>([](const ScriptComponent& lhs, const ScriptComponent& rhs)
					{
						return lhs.entity->GetLayer() > rhs.entity->GetLayer();
					}
				);
				break;
			default:
				K_CORE_WARN("Invalid component type : {}", cp->GetTypeName());
				break;
			}
		}

		return e;
	}


	void Scene::Load(int index)
	{
		K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before loading a new scene");
		Engine::GetInstance()->LoadScene(index);
	}

	void Scene::Load(const char* name)
	{
		K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before loading a new scene");
		Engine::GetInstance()->LoadScene(name);
	}

	void Scene::Pop()
	{
		K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before loading a new scene");
		Engine::GetInstance()->PopScene();
	}

	void Scene::Disable(Entity& e)
	{
		e.m_Active = false;
		EventQueue::Dispatch(new DisableEntity(e));
	}

	void Scene::Enable(Entity& e)
	{
		e.m_Active = true;
		EventQueue::Dispatch(new EnableEntity(e));
	}

	Component* Scene::GetComponent(const ComponentCategory& category, Entity& e)
	{
		Component* ref(nullptr);

		switch (category)
		{
		case ComponentCategory::Transform:
			ref = &m_Registry.get<TransformComponent>(e.GetID());
			break;
		default:
			K_CORE_WARN("Invalid component category : {}", category);
			break;
		}

		return ref;
	}

	const bool Scene::hasComponent(const ComponentCategory &category, Entity& e) const
	{
		switch (category)
		{
		case ComponentCategory::Transform:
			return m_Registry.has<TransformComponent>(e.GetID());
		default:
			K_CORE_WARN("Invalid component category : {}", category);
			return false;
		}
	}

	void Scene::Destroy(Entity& e)
	{
		m_Registry.destroy(e.GetID());

		// Remove reference to entity
		if (m_EntityMap.find(e.GetID()) != m_EntityMap.end()) {
			m_EntityMap.erase(e.GetID());
		}

		EventQueue::Dispatch(new DestroyEntity(e));
	}
} // namespace KGE