#include "headers.h"
#include "ScriptManager.h"
#include "Components.h"
#include "KGE/Engine.h"
#include "KGE/Base.h"
#include "KGE/Events/Events.h"
#include "KGE/Core/Scene.h"

namespace KGE
{

	void ScriptManager::OnEvent(Event& e)
	{
		auto& scene = Engine::GetInstance()->GetCurrentScene();

		if (scene) {
			scene->Reg().view<ScriptComponent>().each([&](auto entity, ScriptComponent& script)
				{
					if (e.handled) return;
					script.OnEvent(e);
				}
			);
		}
	}

	void ScriptManager::OnUpdate(double ts)
	{
		//int count(0);
		auto& scene = Engine::GetInstance()->GetCurrentScene();

		//K_CORE_DEBUG("Updating scripts");
		if (scene) {
			scene->Reg().sort<ScriptComponent>([](const ScriptComponent& lhs, const ScriptComponent& rhs)
				{
					return lhs.entity->GetLayer() > rhs.entity->GetLayer();
				}
			);

			scene->Reg().view<ScriptComponent>()
				.each([&](auto entity, ScriptComponent& script)
					{
						if(script.behaviour) script.OnUpdate(ts);
					}
			);
		}

		//K_CORE_INFO("Updated {} Scripts", count);
	}
} // namespace KGE
