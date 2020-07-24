#pragma once
#include "KGE/Events/Event.h"
#include "ComponentManager.h"
#include "Components.h"
//#include "Runner.h"

namespace KGE
{
	class ScriptManager : public ComponentManager
	{
	public:
		void OnEvent(Event& e) override;

		ScriptManager() = default;

		~ScriptManager() = default;

		void OnUpdate(double ts);

		//private:
		//	std::vector<Ref<BaseRunner>> m_Runners;
	};
} // namespace KGE
