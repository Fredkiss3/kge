//
// Created by Fredkiss3 on 03/07/2020.
//
#include <headers.h>
#include "Component.h"
#include "Components.h"
#include "Entity.h"
#include "Scene.h"

namespace KGE
{
	Component::~Component()
	{
		//K_CORE_ERROR("Deleting component {0} of {1}", type(*this), (entity ? entity->GetName() : "Null"));
	}
} // namespace KGE
