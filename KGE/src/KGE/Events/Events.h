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

	struct WindowResize : public Event
	{
		WindowResize(int w, int h) : width(w), height(h) {

		}

		const std::string GetData() const override
		{
			auto str = std::string("width=") + std::to_string(width) + "px, ";
			str += "Height=" + std::to_string(height) + "px";
			return str;
		};


		int width, height;

		CLASS_TYPE(WindowResize);
	};

	struct FixedUpdate : public Event
	{
		FixedUpdate(double t) : dt(t) {}

		const std::string GetData() const override
		{
			auto str = std::string("delta_time=") + std::to_string(dt) + " s";
			return str;
		};

		double dt;
		CLASS_TYPE(FixedUpdate);
	};


} // namespace KGE