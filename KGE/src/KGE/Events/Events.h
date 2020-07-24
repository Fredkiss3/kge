//
// Created by Fredkiss3 on 04/07/2020.
//
#pragma once

#include "headers.h"
#include "KGE/Events/Event.h"

namespace KGE
{
	struct Init : public Event
	{
		CLASS_TYPE(Init);
	};

	struct EnableEntity : public Event
	{
		EnableEntity(Entity& e)
		{
			entity = Ref<Entity>(&e);
		}

		CLASS_TYPE(EnableEntity);
	};

	struct DisableEntity : public Event
	{
		DisableEntity(Entity& e)
		{
			entity = Ref<Entity>(&e);
		}

		CLASS_TYPE(DisableEntity);
	};

	struct DestroyEntity : public Event
	{
		DestroyEntity(Entity& e)
		{
			entity = Ref<Entity>(&e);
		}

		CLASS_TYPE(DestroyEntity);
	};

	struct Quit : public Event
	{
		CLASS_TYPE(Quit);
	};

	struct StartScene : public Event
	{
		CLASS_TYPE(StartScene);
	};

	struct StopScene : public Event
	{
		CLASS_TYPE(StopScene);
	};

	struct PauseScene : public Event
	{
		CLASS_TYPE(PauseScene);
	};

	struct ContinueScene : public Event
	{
		CLASS_TYPE(ContinueScene);
	};

} // namespace KGE