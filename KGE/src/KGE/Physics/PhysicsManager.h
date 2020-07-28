#pragma once
#include "KGE/Core/ComponentManager.h"
#include "KGE/Events/Events.h"
#include "KGE/Base.h"

namespace KGE
{
	class PhysicsManager : public ComponentManager
	{
	public:
		PhysicsManager();

		void OnDestroyEntity(DestroyEntity& e);

		void OnEnableEntity(EnableEntity& e);

		void OnDisableEntity(DisableEntity& e);

		void OnStartScene(StartScene& e);

		void OnStopScene(StopScene& e);

		void OnPauseScene(PauseScene& e);

		~PhysicsManager()
		{
			//K_CORE_DEBUG("Deleting Physics Manager");
		}

		void OnUpdate(double ts);

	/*	const Scope<b2World>& GetWorld() const
		{

		}*/

	private:
		bool m_Paused = false;
		// Scope<b2World> m_World;
	};
} // namespace KGE