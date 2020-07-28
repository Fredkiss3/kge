#pragma once
#include "KGE/Events/Events.h"
#include "KeyCodes.h"

namespace KGE {

	struct KeyEvent : public Event
	{
	public:
		// Change to custom Code Event
		KeyCode keyCode;
		int mods;
	protected:
		KeyEvent(KeyCode keycode, int mods)
			: keyCode(keycode), mods(mods) {}



		CLASS_TYPE(KeyEvent);
	};

	struct KeyPressed : public KeyEvent
	{
	public:
		KeyPressed(KeyCode keycode, int repeatCount, int mods)
			: KeyEvent(keycode, mods), repeated(repeatCount != 0) {}

		const std::string GetData() const override
		{
			std::stringstream ss;
			ss << "KeyCode=" << keyCode << ", repeated=" << (repeated ? "true" : "false") << ", mods=" << mods;
			return ss.str();
		}

		CLASS_TYPE(KeyPressed);

		bool repeated;
	};

	struct KeyReleased : public KeyEvent
	{
	public:
		KeyReleased(KeyCode keycode, int mods)
			: KeyEvent(keycode, mods) {}

		const std::string GetData() const override
		{
			std::stringstream ss;
			ss << "keyCode=" << keyCode << ", mods=" << mods;
			return ss.str();
		}

		CLASS_TYPE(KeyReleased);
	};

}