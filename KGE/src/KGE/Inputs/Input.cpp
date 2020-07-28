#include "headers.h"
#include "Input.h"
#include "KGE/Graphics/Renderer.h"

namespace KGE {
	bool Input::IsKeyPressed(KeyCode key)
	{
		auto window = Renderer::GetWindow()->GetNativeWindow();
		auto state = glfwGetKey(window, static_cast<int32_t>(key));
		return state == GLFW_PRESS || state == GLFW_REPEAT;
	}
	
	bool Input::IsMousePressed(MouseCode button)
	{
		auto window = Renderer::GetWindow()->GetNativeWindow();
		auto state = glfwGetMouseButton(window, static_cast<int32_t>(button));
		return state == GLFW_PRESS;
	}

	Vec2 Input::GetMousePos()
	{
		auto window = Renderer::GetWindow()->GetNativeWindow();
		double xpos, ypos;
		glfwGetCursorPos(window, &xpos, &ypos);
		return Vec2{ xpos, ypos };
	}
}