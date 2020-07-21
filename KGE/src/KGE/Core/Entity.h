#pragma once
#include "headers.h"
#include "KGE/Base.h"
#include "Component.h"
#include "Hasher.h"

namespace KGE
{
class Scene;

typedef std::vector<Ref<Component>> ComponentList;
class Entity
{
	typedef std::unordered_map<Signature, ComponentList> ComponentMap;
	friend class Scene;

public:
	Entity(const std::string &name = "entity") : m_Name(name),
												 m_ID(0),
												 m_Alive(true),
												 m_Active(true),
												 scene(nullptr)
	{
	}

	~Entity()
	{
		//K_CORE_ERROR("Deleting {}", GetName());
	}

#ifdef K_DEBUG
	void DumpComponents()
	{
		K_CORE_DEBUG("Entity {} has : \n", GetName());
		K_CORE_DEBUG("For Categories : ");
		for (auto &pair : m_CategoryComponentMap)
		{
			for (auto &el : pair.second)
			{
				K_CORE_DEBUG("Component category => {} ", el->GetCategory());
			}
		}

		K_CORE_DEBUG("\nFor Component Types : ");
		for (auto &pair : m_ComponentTypesMap)
		{
			for (auto &el : pair.second)
			{
				K_CORE_DEBUG("Component type => {} ", el->GetType());
			}
		}
	}
#endif

	void addComponent(Component *&c);

	const bool hasComponent(const ComponentCategory &category) const;

	template <ComponentCategory c1, ComponentCategory... Args>
	const bool hasComponent() const;

	const bool hasComponent(const std::string &type) const;

	Ref<Component> GetComponent(const std::string &type);

	ComponentList GetComponents(const std::string &type);

	template <ComponentCategory category>
	Ref<Component> GetComponent();

	Ref<Component> GetComponent(ComponentCategory category);

	ComponentList GetComponents();

	ComponentList GetComponents(ComponentCategory category);

	template <ComponentCategory category>
	ComponentList GetComponents();

	const bool IsActive() const { return m_Active; }

	inline const bool IsAlive() const { return m_ID != 0; }
	const std::string &GetName() const { return m_Name; }

	bool operator==(Entity const &other) const
	{
		return scene == other.scene && m_ID == other.m_ID;
	}

public:
	void destroy();
	void SetActive(bool active);

private:
	const bool hasComponent() const
	{
		return true;
	}

private:
	size_t m_ID;
	Ref<Scene> scene;
	ComponentMap m_CategoryComponentMap;
	ComponentMap m_ComponentTypesMap;
	bool m_Alive;
	bool m_Active;

	Signature m_ComponentSignature;
	Signature m_CategorySignature;
	std::string m_Name;
};

template <ComponentCategory c1, ComponentCategory... Args>
inline const bool Entity::hasComponent() const
{
	return hasComponent(c1) && hasComponent(Args...);
}

template <ComponentCategory category>
inline ComponentList Entity::GetComponents()
{
	return GetComponents(category);
}

template <ComponentCategory category>
inline Ref<Component> Entity::GetComponent()
{
	return GetComponent(category);
}

} // namespace KGE