//
// Created by Fredkiss3 on 03/07/2020.
//
#include <headers.h>
#include "Component.h"
#include "Components.h"
#include "Scene.h"
#include "Entity.h"

namespace KGE {

	Ref<Component> Component::GetComponent(const char* type)
	{
        Ref<Component> result = nullptr;
        if (entity) {
            result = entity->GetComponent(type);
        }
		return result;
	}
	Ref<Component> Component::GetComponent(ComponentCategory category)
	{
		Ref<Component> result = nullptr;
		if (entity) {
			result = entity->GetComponent(category);
		}
		return result;
	}

	Component::~Component()
	{
		K_CORE_ERROR("Deleting component {0} of {1}", type(*this), (entity ? entity->GetName() : "Null"));
	}
}
