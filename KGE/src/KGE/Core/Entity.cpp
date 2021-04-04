#include <headers.h>
#include "Entity.h"
#include "Components.h"
#include "Scene.h"

namespace KGE
{
	void Entity::SetActive(bool active)
	{
		m_Active = active;
		if (m_Scene != nullptr)
		{
			if (active)
			{
				m_Scene->Enable(*this);
			}
			else
			{
				m_Scene->Disable(*this);
			}
		}
	}

	void Entity::destroy()
	{
		if (m_Scene != nullptr)
		{
			m_Scene->Destroy(*this);
		}
	}

	const std::string& Entity::tag() const { 
		return m_Scene->Reg().get<TagComponent>(m_ID).tag;
	}

	TransformComponent& Entity::xf() const {
		return m_Scene->Reg().get<TransformComponent>(m_ID); 
	}

	bool Entity::operator==(Entity const& other) const
	{
		return m_Scene == other.m_Scene && m_ID == other.m_ID;
	}

	bool Entity::operator==(Entity& other) const
	{
		return m_Scene == other.m_Scene && m_ID == other.m_ID;
	}

} // namespace KGE