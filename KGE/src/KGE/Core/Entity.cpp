#include <headers.h>
#include "Entity.h"
#include "Components.h"
#include "Scene.h"

namespace KGE
{
	void Entity::SetActive(bool active) {
		m_Active = active;
		if (scene != nullptr) {
			if (active) {
				scene->Enable(*this);
			}
			else {
				scene->Disable(*this);
			}
		}
	}

	void Entity::destroy() {
		if (scene != nullptr) {
			scene->remove(*this);
		}
	}

	void Entity::addComponent(Component* c) {
		Ref<Component> ref(c);
		ref->entity = this;

		m_CategorySignature = Hasher::computeSignature(c->GetCategory(), m_CategorySignature);
		m_ComponentSignature = Hasher::computeSignature(c->GetType(), m_ComponentSignature);

		// add component to components
		auto& bit1 = Hasher::getSignature(c->GetType());
		auto& bit2 = Hasher::getSignature(c->GetCategory());
		m_ComponentTypesMap[bit1].push_back(ref);
		m_CategoryComponentMap[bit2].push_back(ref);
	}

	const bool Entity::hasComponent(const ComponentCategory& category) const {
		auto& bit2 = Hasher::getSignature(category);
		auto& bit1 = m_CategorySignature;
		bool has = (bit1 & bit2) == bit2;
		return (bit1 & bit2) == bit2;
	}

	const bool Entity::hasComponent(const std::string& type) const {
		auto& bit2 = Hasher::getSignature(type);
		auto& bit1 = m_ComponentSignature;
		return (bit1 & bit2) == bit2;
	}

	Ref<Component> Entity::GetComponent(const std::string& type) {
		Ref<Component> ref = nullptr;

		if (hasComponent(type)) {
			// Get type signature
			auto& cMap = m_ComponentTypesMap;
			auto& sign = Hasher::getSignature(type);

			// if signature has been found then get the first component of this type
			auto& it = cMap.find(sign);
			if (it != cMap.end()) {
				auto& cList = it->second;
				if (cList.size() > 0) {
					ref = cList[0];
				}
			}
		}
		return ref;
	}

	ComponentList Entity::GetComponents(const std::string& type)
	{
		ComponentList ref;

		if (hasComponent(type))
		{
			// Get type signature
			auto& cMap = m_ComponentTypesMap;
			auto& sign = Hasher::getSignature(type);

			// if signature has been found then get the first component of this type
			auto& it = cMap.find(sign);
			if (it != cMap.end())
			{
				auto& cList = it->second;
				if (cList.size() > 0)
				{
					ref = cList;
				}
			}
		}
		return ref;
	}

	Ref<Component> Entity::GetComponent(ComponentCategory category)
	{
		Ref<Component> ref = nullptr;
		if (hasComponent(category))
		{
			auto& cMap = m_CategoryComponentMap;
			auto& sign = Hasher::getSignature(category);

			// if signature has been found then get the first component of this type
			auto& it = cMap.find(sign);
			if (it != cMap.end())
			{
				auto& cList = it->second;
				if (cList.size() > 0)
				{
					ref = cList[0];
				}
			}
		}

		return ref;
	}

	ComponentList Entity::GetComponents() {
		ComponentList ref;
		return ref;
	}

	ComponentList Entity::GetComponents(ComponentCategory category) {
		ComponentList ref;

		// if signature has been found then get the first component of this type
		if (hasComponent(category)) {
			auto& cMap = m_CategoryComponentMap;
			auto& sign = Hasher::getSignature(category);

			// if signature has been found then get the first component of this type
			auto& it = cMap.find(sign);
			if (it != cMap.end()) {
				auto& cList = it->second;
				if (cList.size() > 0) {
					ref = cList;
				}
			}
		}

		return ref;
	}

} // namespace KGE