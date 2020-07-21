#pragma once
#include "KGE/Core/ComponentManager.h"
#include "KGE/Core/Components.h"
#include "KGE/Events/Events.h"

namespace KGE
{
class PhysicsManager : public ComponentManager
{
public:
	void OnEvent(Event const &e);

	void OnDestroyEntity(DestroyEntity const &e);

	void OnEnableEntity(EnableEntity const &e);

	void OnDisableEntity(DisableEntity const &e);

	void OnStartScene(StartScene const &e);

	void OnStopScene(StopScene const &e);

	void OnPauseScene(PauseScene const &e);

	PhysicsManager() = default;

	~PhysicsManager()
	{
		//K_CORE_DEBUG("Deleting Physics Manager");
	}

	void OnUpdate(double ts);

private:
	bool m_Paused = false;
	// Scope<b2World> m_World;
};
} // namespace KGE