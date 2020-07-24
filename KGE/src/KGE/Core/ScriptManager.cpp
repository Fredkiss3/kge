#include "headers.h"
#include "ScriptManager.h"
#include "Components.h"
#include "KGE/Engine.h"
#include "KGE/Base.h"
#include "KGE/Events/Events.h"

namespace KGE
{

	void ScriptManager::OnEvent(Event& e)
	{
		auto& scene = Engine::GetInstance()->GetCurrentScene();
		K_CORE_DEBUG("Sending event {} to scripts", e.Print());

		if (scene) {
			scene->Reg().view<ScriptComponent>()
				.each([&](auto entity, ScriptComponent& script)
					{
						script.OnEvent(e);
					}
			);
		}

		K_CORE_DEBUG("event sent");
	}

	void ScriptManager::OnUpdate(double ts)
	{
		//int count(0);
		auto& scene = Engine::GetInstance()->GetCurrentScene();

		//K_CORE_DEBUG("Updating scripts");
		if (scene) {
			scene->Reg().view<ScriptComponent>()
				.each([&](auto entity, ScriptComponent& script)
					{
						script.OnUpdate(ts);
					}
			);
		}
		
		//K_CORE_INFO("Updated {} Scripts", count);
	}
} // namespace KGE
