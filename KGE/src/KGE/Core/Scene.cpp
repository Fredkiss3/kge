#include "headers.h"
#include "Scene.h"
#include "Entity.h"
#include "KGE/Engine.h"
#include "entt/entt.hpp"
#include "KGE/Graphics/Components.h"

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

	void Scene::setUp() 
	{	
		K_CORE_ASSERT(!m_Started, "Should stop the scene before starting a new scene !");
		K_CORE_TRACE("Setting Up the Scene '{}'", GetName());
		// TODO should dispatch events
		
		// Creating the main Camera
		m_MainCamera = Create({ "Main Camera" });
		/*auto id = m_Registry.create();
		m_MainCamera = Entity(id);
		m_MainCamera.m_Scene = this;
		m_Registry.emplace<TransformComponent>(id);
		auto& tag = m_Registry.emplace<TagComponent>(id);
		tag.tag = "Main Camera";*/
		auto& cc = m_MainCamera.AddComponent<CameraComponent>();
		cc.Primary = true;
		cc.FixedAspectRatio = false;

		EventQueue::Dispatch(new StartScene, true);

		m_SetupFn(this);
		m_Started = true;
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

	Entity& Scene::Create(const EntityData& data)
	{
		K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before adding an entity");

		auto id = m_Registry.create();

		// Keep a reference to entity in order to prevent it from deletion
		m_EntityMap[id] = Entity(id);
		auto& e = m_EntityMap[id];

		e.m_Scene = this;

		// add a transform, set tag & stuff
		auto& xf = data.xf;
		auto& tf = e.AddComponent<TransformComponent>(xf.pos, xf.scale, xf.rotation);
		/*tf.entity = &e;
		tf.pos = xf.pos;
		tf.scale = xf.scale;
		tf.rotation = xf.rotation;*/

		auto& tag = e.AddComponent<TagComponent>(data.Tag.empty() ? "Empty" : data.Tag);
		//tag.tag = data.Tag.empty() ? "Empty" : data.Tag;

		// Add script
		if (data.GetScript()) {
			auto& sc = m_Registry.emplace<ScriptComponent>(e);
			sc.entity = &e;
			sc.Attach(data.GetScript());
		}

		// add components to registry
		AddComponents(data.GetComponents(), e);

		return e;
	}
	
	Entity& Scene::Create()
	{
		K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before adding an entity");
		return Create(EntityData());
	}
	
	void Scene::AddComponents(const std::vector<Component*>& cps, Entity& e) {
		for (auto& cp : cps)
		{
			cp->entity = &e;

			switch (cp->GetCategory())
			{
			case ComponentCategory::Sprite:
			{
				auto& cp2 = dynamic_cast<SpriteComponent&>(*cp);
				e.AddComponent<SpriteComponent>(cp2.color, cp2.texture);

				break;
			}
			case ComponentCategory::Camera:
			{
				auto& cp3 = dynamic_cast<CameraComponent&>(*cp);
				e.AddComponent<CameraComponent>(cp3.GetProjection());
				break;
			}
			default:
				K_CORE_WARN("Invalid component type : {}", cp->GetTypeName());
				break;
			}
		}
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

	void Scene::Destroy(Entity& e)
	{
		m_Registry.destroy(e.GetID());

		// Remove reference to entity
		/*if (m_EntityMap.find(e.GetID()) != m_EntityMap.end()) {
			m_EntityMap.erase(e.GetID());
		}*/

		// Deactivate & Shut down the entity
		e.m_Active = false;
		e.m_Alive = false;

		EventQueue::Dispatch(new DestroyEntity(e));
	}
} // namespace KGE