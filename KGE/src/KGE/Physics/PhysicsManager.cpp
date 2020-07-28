#include "headers.h"
#include "PhysicsManager.h"
//#include "KGE/Engine.h"
//#include "KGE/Events/Events.h"

namespace KGE
{

	PhysicsManager::PhysicsManager()
	{
		Bind<DestroyEntity>(K_BIND_EVENT_FN(PhysicsManager::OnDestroyEntity));
		Bind<EnableEntity>(K_BIND_EVENT_FN(PhysicsManager::OnEnableEntity));
		Bind<DisableEntity>(K_BIND_EVENT_FN(PhysicsManager::OnDisableEntity));
		Bind<StartScene>(K_BIND_EVENT_FN(PhysicsManager::OnStartScene));
		Bind<StopScene>(K_BIND_EVENT_FN(PhysicsManager::OnStopScene));
		Bind<PauseScene>(K_BIND_EVENT_FN(PhysicsManager::OnPauseScene));
	}

	void PhysicsManager::OnUpdate(double ts)
	{
		// Update the world
		//K_CORE_DEBUG("Physics Update !!");
	}

	void PhysicsManager::OnDestroyEntity(DestroyEntity& e)
	{
		// Destroy the rb and colliders attached
	}

	void PhysicsManager::OnEnableEntity(EnableEntity& e)
	{
		// Enable the Rb & colliders
	}

	void PhysicsManager::OnDisableEntity(DisableEntity& e)
	{
		// Disable the Rb & colliders
	}

	void PhysicsManager::OnStartScene(StartScene& e)
	{
		// Assign the world
	}

	void PhysicsManager::OnStopScene(StopScene& e)
	{
		// Set the world to NULL
	}

	void PhysicsManager::OnPauseScene(PauseScene& e)
	{
		// Pause the world
	}
} // namespace KGE
