#pragma once

namespace KGE
{
	typedef enum class MouseCode : uint16_t
	{
		// From glfw3.h
		Button0 = 0,
		Button1 = 1,
		Button2 = 2,
		Button3 = 3,
		Button4 = 4,
		Button5 = 5,
		Button6 = 6,
		Button7 = 7,

		ButtonLast = Button7,
		ButtonLeft = Button0,
		ButtonRight = Button1,
		ButtonMiddle = Button2
	} Mouse;

	inline std::ostream& operator<<(std::ostream& os, MouseCode mouseCode)
	{
		os << static_cast<int32_t>(mouseCode);
		return os;
	}
}

#define K_MOUSE_BUTTON_0      ::KGE::Mouse::Button0
#define K_MOUSE_BUTTON_1      ::KGE::Mouse::Button1
#define K_MOUSE_BUTTON_2      ::KGE::Mouse::Button2
#define K_MOUSE_BUTTON_3      ::KGE::Mouse::Button3
#define K_MOUSE_BUTTON_4      ::KGE::Mouse::Button4
#define K_MOUSE_BUTTON_5      ::KGE::Mouse::Button5
#define K_MOUSE_BUTTON_6      ::KGE::Mouse::Button6
#define K_MOUSE_BUTTON_7      ::KGE::Mouse::Button7
#define K_MOUSE_BUTTON_LAST   ::KGE::Mouse::ButtonLast
#define K_MOUSE_BUTTON_LEFT   ::KGE::Mouse::ButtonLeft
#define K_MOUSE_BUTTON_RIGHT  ::KGE::Mouse::ButtonRight
#define K_MOUSE_BUTTON_MIDDLE ::KGE::Mouse::ButtonMiddle
