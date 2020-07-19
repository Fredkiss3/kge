#pragma once
#include "ComponentManager.h"
#include "Components.h"

namespace KGE {
	class ScriptManager : public ComponentManager
	{
	public:
		void OnEvent(Event const& e);
		
		ScriptManager() = default;

		~ScriptManager()
		{
			//K_CORE_DEBUG("Deleting Script Manager");
		}

		void OnUpdate(double ts);
	};
}
