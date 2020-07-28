#pragma once
#include "headers.h"
#include "KGE/Base.h"
#include "Component.h"
#include "Components.h"
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
			m_Name("Entity"),
			m_Active(true),
			scene(nullptr),
			m_Layer(0)
		{
		}

		Entity(entt::entity&& ID)
			: m_ID(ID),
			m_Name("Entity"),
			m_Active(true),
			scene(nullptr),
			m_Layer(0)
		{
		}

		Entity(const std::string& name = "entity", int layer = 0)
			: m_Name(name),
			m_Active(true),
			m_ID(entt::null),
			scene(nullptr),
			m_Layer(layer)
		{
		}

		operator const entt::entity& ()
		{
			return m_ID;
		}

		~Entity()
		{
			//K_CORE_ERROR("Deleting {}", GetName());
		}


		// template <ComponentCategory c1, ComponentCategory... Args>
		//const bool hasComponent() const;

		const bool hasComponent(const ComponentCategory &category);
		const bool hasBehaviour(const std::string &type) const;

		Behaviour* GetBehaviour(const std::string& type);

		Component* GetComponent(ComponentCategory category);

		//template <ComponentCategory category>
		//Ref<Component> GetComponent()
		//{
		//	return GetComponent(category);
		//}

		void SetLayer(int layer) 
		{
			K_CORE_ASSERT(layer >= 0, "Layer should be positive !");
			m_Layer = layer; 
		}

		const int GetLayer() const  { return m_Layer; }

		const bool IsActive() const { return m_Active; }

		const bool IsAlive() const;

		const std::string& GetName() const { return m_Name; }

		const std::string& GetTag() const { return m_Tag; }

		entt::entity GetID() { return m_ID; }
		
		TransformComponent& GetXF();

		bool operator==(Entity const& other) const
		{
			return scene == other.scene && m_ID == other.m_ID;
		}

		bool operator==(Entity& other) const
		{
			return scene == other.scene && m_ID == other.m_ID;
		}

	public:
		void destroy();
		void SetActive(bool active);

		TransformComponent transform;
	private:
		const bool hasComponent() const
		{
			return true;
		}

	private:
		int m_Layer;
		entt::entity m_ID;
		Scene* scene = nullptr;

		std::string m_Name;
		std::string m_Tag;

		bool m_Active;
	};
} // namespace KGE