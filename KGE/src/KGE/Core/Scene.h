#pragma once
#include "entt/entt.hpp"
#include "KGE/Core/Entity.h"
#include "KGE/Events/Events.h"
#include "KGE/Core/Components.h"
#include "KGE/Base.h"

namespace KGE
{
	class Engine;

	class EntityData
	{
	public:
		~EntityData()
		{
			//K_CORE_ERROR("Deleting data of entity {}", m_Name);
		}

		virtual const std::vector<Component*> GetComponents() const
		{
			return { };
		};

		virtual const char* GetName() const 
		{
			return "empty entity";
		}

		virtual const char* GetTag() const
		{
			return "empty";
		}

		virtual const TransformComponent GetXf() const
		{
			return TransformComponent();
		}

		friend class Entity;
		friend class Scene;
	};

	class Scene
	{
		typedef std::function<void(Scene*)> SetupFn;

	public:
		Scene(const SetupFn& fn, const std::string& name = "new Scene");
		~Scene();

		void setUp()
		{
			K_CORE_ASSERT(!m_Started, "Should stop the scene before starting a new scene !");
			K_CORE_TRACE("Setting Up the Scene '{}'", GetName());
			// TODO should dispatch events
			EventQueue::Dispatch(new StartScene, true);

			m_SetupFn(this);
			m_Started = true;
		};

		void tearDown()
		{
			K_CORE_ASSERT(m_Started, "Should start the scene before tearing it down !");
			K_CORE_TRACE("Tearing Down '{}'", GetName());

			// TODO should dispatch events
			EventQueue::Dispatch(new StopScene, true);
			m_Started = false;
		};

		std::string GetName() { return m_Name; }

		Entity& Create(EntityData& data);
		//Entity& Create(EntityData&& data);

		void Destroy(Entity& e);

		void Disable(Entity& e);

		void Enable(Entity& e);

		Component* GetComponent(const ComponentCategory& category, Entity& e);

		const bool hasComponent(const ComponentCategory& category, Entity& e) const;

		entt::registry& Reg() { return m_Registry; }

	public:
		// STATIC METHODS
		static void Pause()
		{
			EventQueue::Dispatch(new PauseScene, true);
		};

		static void Continue()
		{
			EventQueue::Dispatch(new ContinueScene, true);
		};

		// Allow full control of scene in Engine
		friend class Engine;

		// Start a new scene
		static void Load(int index);
		static void Load(const char* name);
		static void Pop();

	private:
		std::string m_Name = "new Scene";
		bool m_Started = false;
		SetupFn m_SetupFn;
		entt::registry m_Registry;

		std::unordered_map < entt::entity, Entity> m_EntityMap;
	};
} // namespace KGE