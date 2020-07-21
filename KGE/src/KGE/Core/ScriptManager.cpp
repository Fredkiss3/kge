#include "headers.h"
#include "ScriptManager.h"
#include "Components.h"
#include "KGE/Engine.h"
#include "KGE/Base.h"
#include "KGE/Events/Events.h"

namespace KGE
{

void ScriptManager::OnEvent(Event const &e)
{
	auto &scene = Engine::GetInstance()->GetCurrentScene();

	K_CORE_DEBUG("Sending event {} to scripts", e.Print());

	scene->each<ComponentCategory::Behaviour>([&](Entity &entity) {
		for (auto cp : entity.GetComponents(ComponentCategory::Behaviour))
		{
			if (cp)
			{
				castRef<Behaviour>(cp).OnEvent(e);
			}
		}
	});

	K_CORE_DEBUG("event sent");
}

void ScriptManager::OnUpdate(double ts)
{
	int count(0);
	auto &scene = Engine::GetInstance()->GetCurrentScene();

	//K_CORE_DEBUG("Updating scripts");

	scene->each<ComponentCategory::Behaviour>([&count, ts](Entity &entity) {
		for (auto cp : entity.GetComponents(ComponentCategory::Behaviour))
		{
			if (cp)
			{
				castRef<Behaviour>(cp).OnUpdate(ts);
				// ++count;
			}
		}
	});

	//K_CORE_INFO("Updated {} Scripts", count);
}
} // namespace KGE
