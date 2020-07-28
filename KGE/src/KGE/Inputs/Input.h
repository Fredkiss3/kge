#pragma once
#include <GLFW/glfw3.h>
#include "KeyCodes.h"
#include "MouseCodes.h"
#include "KGE/Utils/Math.h"

namespace KGE {
	class Input
	{
	public:
		static bool IsKeyPressed(KeyCode key);
		
		static bool IsMousePressed(MouseCode button);
		
		static Vec2 GetMousePos();
	};
}