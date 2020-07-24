//
// Created by Fredkiss3 on 03/07/2020.
//
#include <headers.h>
#include "Component.h"
#include "Components.h"
#include "Scene.h"
#include "Entity.h"

namespace KGE
{

	Behaviour* Component::GetBehaviour(const std::string& type)
	{
		return entity ? entity->GetBehaviour(type) : nullptr;
	}

	Component* Component::GetComponent(ComponentCategory category)
	{
		return entity ? entity->GetComponent(category) : nullptr;
	}

	const bool Component::HasBehaviour(const std::string& type) const
	{
		return entity ? entity->hasBehaviour(type) : false;
	}

	const bool Component::HasComponent(ComponentCategory category) const
	{
		return entity ? entity->hasComponent(category) : false;
	}

	Component::~Component()
	{
		//K_CORE_ERROR("Deleting component {0} of {1}", type(*this), (entity ? entity->GetName() : "Null"));
	}
} // namespace KGE
