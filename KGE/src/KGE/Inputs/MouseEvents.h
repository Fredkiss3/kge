#pragma once
#include "headers.h"
#include "KGE/Events/Events.h"
#include "KGE/Utils/Math.h"
#include "MouseCodes.h"

namespace KGE {

	struct MouseMoved : public Event
	{
		Vec2 pos;
	public:
		MouseMoved(double x, double y)
			: pos{x, y} {}

		const std::string GetData() const override
		{
			std::stringstream ss;
			ss << "pos=(" << pos.x << "px, " << pos.y << "px)";
			return ss.str();
		}

		CLASS_TYPE(MouseMoved);
	};

	struct MouseScrolled : public Event
	{
		Vec2 offset;
	public:
		MouseScrolled(double xOffset, double yOffset)
			: offset{xOffset, yOffset} {}

		const std::string GetData() const override
		{
			std::stringstream ss;
			ss << "offset=(" << offset.x << "px, " << offset.y << "px)";
			return ss.str();
		}

		CLASS_TYPE(MouseScrolled);
	};

	struct MouseButtonEvent : public Event
	{
	public:
		MouseCode button;
		int mods;

		virtual const std::string GetData() const override
		{
			std::stringstream ss;
			ss << "button=" << button << ", mods=" << mods;
			return ss.str();
		}

	protected:
		MouseButtonEvent(MouseCode button, int mods)
			: button(button), mods(mods) {}
		CLASS_TYPE(MouseButtonEvent)
	};

	struct MousePressed : public MouseButtonEvent
	{
	public:
		MousePressed(MouseCode button, int mods)
			: MouseButtonEvent(button, mods) {}

		CLASS_TYPE(MousePressed);
	};

	struct MouseReleased : public MouseButtonEvent
	{
	public:
		MouseReleased(MouseCode button, int mods)
			: MouseButtonEvent(button, mods) {}

		CLASS_TYPE(MouseReleased);
	};

}