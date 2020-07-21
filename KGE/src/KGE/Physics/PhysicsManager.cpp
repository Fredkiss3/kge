#include "headers.h"
#include "PhysicsManager.h"
#include "KGE/Engine.h"

namespace KGE
{

void PhysicsManager::OnEvent(Event const &e)
{
    auto &scene = Engine::GetInstance()->GetCurrentScene();

    // delegate to event handlers
    // switch (e.GetType())
    // {
    // case EVENT_TYPE(DestroyEntity):
    //     OnDestroyEntity(*(dynamic_cast<DestroyEntity>(e)));
    //     break;
    // default:
    //     break;
    // }
}

void PhysicsManager::OnUpdate(double ts)
{
    // Update the world
}

void OnDestroyEntity(DestroyEntity const &e)
{
    // Destroy the rb and colliders attached
}

void OnEnableEntity(EnableEntity const &e)
{
    // Enable the Rb & colliders
}

void OnDisableEntity(DisableEntity const &e)
{
    // Disable the Rb & colliders
}

void OnStartScene(StartScene const &e)
{
    // Assign the world
}

void OnStopScene(StopScene const &e)
{
    // Set the world to NULL
}

void OnPauseScene(PauseScene const &e)
{
    // Pause the world
}
} // namespace KGE
