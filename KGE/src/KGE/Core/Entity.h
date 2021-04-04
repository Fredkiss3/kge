#pragma once
#include "headers.h"
#include "KGE/Base.h"
#include "Component.h"
#include "Components.h"
//#include "KGE/Core/Scene.h"

#include <entt/entt.hpp>

namespace KGE
{
	class Scene;

	class Entity
	{
		friend class Scene;

	public:
		Entity(entt::entity& ID)
			: m_ID(ID),
			m_Active(true),
			m_Alive(true),
			m_Scene(nullptr),
			m_Layer(0)
		{
		}

		Entity(entt::entity&& ID)
			: m_ID(ID),
			m_Active(true),
			m_Alive(true),
			m_Scene(nullptr),
			m_Layer(0)
		{
		}

		Entity(int layer = 0)
			: m_Active(true),
			m_ID(entt::null),
			m_Alive(true),
			m_Scene(nullptr),
			m_Layer(layer)
		{
			K_CORE_ASSERT(layer >= 0, "Layer should be positive !");
		}

		~Entity()
		{
			//K_CORE_ERROR("Deleting {}", GetName());
		}

	public:
		const bool IsAlive() const { return m_Alive; };
		
	public:
		// CRUD Components & Behaviours
		template<typename T>
		T& GetComponent() const
		{
			K_CORE_ASSERT(hasComponent<T>(), "Entity does not have component!");
			return m_Scene->Reg().get<T>(m_ID);
		}

		template<typename T>
		T& GetBehaviour() const
		{
			K_CORE_ASSERT(hasComponent<ScriptComponent>(), "Entity does not have a native script attached!");
			return dynamic_cast<T&>(*(m_Scene->Reg().get<ScriptComponent>(m_ID).behaviour));
		}


		template<typename T>
		bool hasBehaviour() const
		{
			return hasComponent<ScriptComponent>() && typeid(T) == typeid(*(m_Scene->Reg().get<ScriptComponent>(m_ID).behaviour));
		}

		template<typename T>
		bool hasComponent() const
		{
			return m_Scene->Reg().has<T>(m_ID); 
		}

		template<typename T, typename... Args>
		T& AddComponent(Args&&... args)
		{
			K_CORE_ASSERT(!hasComponent<T>(), "Entity already has component!");
			T& cp = m_Scene->Reg().emplace<T>(m_ID, std::forward<Args>(args)...);
			cp.entity = this;
			return cp;
		}

		template<typename T, typename... Args>
		void AddBehavior(Args&&... args)
		{
			K_CORE_ASSERT(!hasBehaviour<T>(), "Entity already has this script!");
			auto & cp = m_Scene->Reg().emplace<ScriptComponent>(m_ID);
			cp.entity = this;
			cp.Attach<T>(std::forward<Args>(args)...);
		}
		
		template<typename T, typename... Args>
		void AddBehaviour(Args&&... args)
		{
			AddBehavior<T>(std::forward<Args>(args)...);
		}


		template<typename T>
		void RemoveComponent()
		{
			K_CORE_ASSERT(hasComponent<T>(), "Entity does not have component!");
			m_Scene->Reg().remove<T>(m_ID);
		}

	public:
		void SetLayer(int layer) 
		{
			K_CORE_ASSERT(layer >= 0, "Layer should be positive !");
			m_Layer = layer; 
		}

		const int GetLayer() const  { return m_Layer; }

		const bool IsActive() const { return m_Active; }

		
		const std::string& tag() const;
		Scene* GetScene() const { return m_Scene; }

		entt::entity GetID() { return m_ID; }
		
		TransformComponent& xf() const;

		bool operator==(Entity const& other) const;

		bool operator==(Entity& other) const;

		operator const entt::entity& ()
		{
			return m_ID;
		}


	public:
		void destroy();
		void SetActive(bool active);

	private:
		int m_Layer;
		entt::entity m_ID;
		Scene* m_Scene = nullptr;

		bool m_Active;
		bool m_Alive;
	};
} // namespace KGE