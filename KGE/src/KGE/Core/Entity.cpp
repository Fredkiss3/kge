#include <headers.h>
#include "Entity.h"
#include "Components.h"
#include "Scene.h"

namespace KGE
{
	void Entity::SetActive(bool active)
	{
		m_Active = active;
		if (scene != nullptr)
		{
			if (active)
			{
				scene->Enable(*this);
			}
			else
			{
				scene->Disable(*this);
			}
		}
	}

	void Entity::destroy()
	{
		if (scene != nullptr)
		{
			scene->Destroy(*this);
		}
	}

	Behaviour* Entity::GetBehaviour(const std::string& type)
	{
		if (!scene) return nullptr;
		if (!scene->Reg().has<ScriptComponent>(m_ID)) return nullptr;

		auto& b = scene->Reg().get<ScriptComponent>(m_ID).Get(type);
		return &(*b);
	}

	Component* Entity::GetComponent(ComponentCategory category)
	{
		if (!scene) return nullptr;

		//auto cp = scene->GetComponent(category, *this);
		return scene->GetComponent(category, *this);
	}

	const bool Entity::IsAlive() const
	{
		if (scene == nullptr)
			return false;

		return scene->Reg().valid(m_ID);
	}

	const bool Entity::hasComponent(const ComponentCategory& category) {
		if (!scene) return false;

		return scene->hasComponent(category, *this);
	}

	const bool Entity::hasBehaviour(const std::string& type) const {
		if (!scene) return false;

		return scene->Reg().has<ScriptComponent>(m_ID) ?
			scene->Reg().get<ScriptComponent>(m_ID).Has(type) : false;
	}

	TransformComponent& Entity::GetXF() {
		return scene->Reg().get<TransformComponent>(m_ID);
	}

} // namespace KGE