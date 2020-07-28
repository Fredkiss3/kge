#pragma once

namespace KGE
{
	typedef enum class KeyCode : uint16_t
	{
		// From glfw3.h
		Space = 32,
		Apostrophe = 39, /* ' */
		Comma = 44, /* , */
		Minus = 45, /* - */
		Period = 46, /* . */
		Slash = 47, /* / */

		D0 = 48, /* 0 */
		D1 = 49, /* 1 */
		D2 = 50, /* 2 */
		D3 = 51, /* 3 */
		D4 = 52, /* 4 */
		D5 = 53, /* 5 */
		D6 = 54, /* 6 */
		D7 = 55, /* 7 */
		D8 = 56, /* 8 */
		D9 = 57, /* 9 */

		Semicolon = 59, /* ; */
		Equal = 61, /* = */

		A = 65,
		B = 66,
		C = 67,
		D = 68,
		E = 69,
		F = 70,
		G = 71,
		H = 72,
		I = 73,
		J = 74,
		K = 75,
		L = 76,
		M = 77,
		N = 78,
		O = 79,
		P = 80,
		Q = 81,
		R = 82,
		S = 83,
		T = 84,
		U = 85,
		V = 86,
		W = 87,
		X = 88,
		Y = 89,
		Z = 90,

		LeftBracket = 91,  /* [ */
		Backslash = 92,  /* \ */
		RightBracket = 93,  /* ] */
		GraveAccent = 96,  /* ` */

		World1 = 161, /* non-US #1 */
		World2 = 162, /* non-US #2 */

		/* Function keys */
		Escape = 256,
		Enter = 257,
		Tab = 258,
		Backspace = 259,
		Insert = 260,
		Delete = 261,
		Right = 262,
		Left = 263,
		Down = 264,
		Up = 265,
		PageUp = 266,
		PageDown = 267,
		Home = 268,
		End = 269,
		CapsLock = 280,
		ScrollLock = 281,
		NumLock = 282,
		PrintScreen = 283,
		Pause = 284,
		F1 = 290,
		F2 = 291,
		F3 = 292,
		F4 = 293,
		F5 = 294,
		F6 = 295,
		F7 = 296,
		F8 = 297,
		F9 = 298,
		F10 = 299,
		F11 = 300,
		F12 = 301,
		F13 = 302,
		F14 = 303,
		F15 = 304,
		F16 = 305,
		F17 = 306,
		F18 = 307,
		F19 = 308,
		F20 = 309,
		F21 = 310,
		F22 = 311,
		F23 = 312,
		F24 = 313,
		F25 = 314,

		/* Keypad */
		KP0 = 320,
		KP1 = 321,
		KP2 = 322,
		KP3 = 323,
		KP4 = 324,
		KP5 = 325,
		KP6 = 326,
		KP7 = 327,
		KP8 = 328,
		KP9 = 329,
		KPDecimal = 330,
		KPDivide = 331,
		KPMultiply = 332,
		KPSubtract = 333,
		KPAdd = 334,
		KPEnter = 335,
		KPEqual = 336,

		LeftShift = 340,
		LeftControl = 341,
		LeftAlt = 342,
		LeftSuper = 343,
		RightShift = 344,
		RightControl = 345,
		RightAlt = 346,
		RightSuper = 347,
		Menu = 348
	} Key;

	inline std::ostream& operator<<(std::ostream& os, KeyCode keyCode)
	{
		os << static_cast<int32_t>(keyCode);
		return os;
	}
}

// From glfw3.h
#define K_KEY_SPACE           ::KGE::Key::Space
#define K_KEY_APOSTROPHE      ::KGE::Key::Apostrophe    /* ' */
#define K_KEY_COMMA           ::KGE::Key::Comma         /* , */
#define K_KEY_MINUS           ::KGE::Key::Minus         /* - */
#define K_KEY_PERIOD          ::KGE::Key::Period        /* . */
#define K_KEY_SLASH           ::KGE::Key::Slash         /* / */
#define K_KEY_0               ::KGE::Key::D0
#define K_KEY_1               ::KGE::Key::D1
#define K_KEY_2               ::KGE::Key::D2
#define K_KEY_3               ::KGE::Key::D3
#define K_KEY_4               ::KGE::Key::D4
#define K_KEY_5               ::KGE::Key::D5
#define K_KEY_6               ::KGE::Key::D6
#define K_KEY_7               ::KGE::Key::D7
#define K_KEY_8               ::KGE::Key::D8
#define K_KEY_9               ::KGE::Key::D9
#define K_KEY_SEMICOLON       ::KGE::Key::Semicolon     /* ; */
#define K_KEY_EQUAL           ::KGE::Key::Equal         /* = */
#define K_KEY_A               ::KGE::Key::A
#define K_KEY_B               ::KGE::Key::B
#define K_KEY_C               ::KGE::Key::C
#define K_KEY_D               ::KGE::Key::D
#define K_KEY_E               ::KGE::Key::E
#define K_KEY_F               ::KGE::Key::F
#define K_KEY_G               ::KGE::Key::G
#define K_KEY_H               ::KGE::Key::H
#define K_KEY_I               ::KGE::Key::I
#define K_KEY_J               ::KGE::Key::J
#define K_KEY_K               ::KGE::Key::K
#define K_KEY_L               ::KGE::Key::L
#define K_KEY_M               ::KGE::Key::M
#define K_KEY_N               ::KGE::Key::N
#define K_KEY_O               ::KGE::Key::O
#define K_KEY_P               ::KGE::Key::P
#define K_KEY_Q               ::KGE::Key::Q
#define K_KEY_R               ::KGE::Key::R
#define K_KEY_S               ::KGE::Key::S
#define K_KEY_T               ::KGE::Key::T
#define K_KEY_U               ::KGE::Key::U
#define K_KEY_V               ::KGE::Key::V
#define K_KEY_W               ::KGE::Key::W
#define K_KEY_X               ::KGE::Key::X
#define K_KEY_Y               ::KGE::Key::Y
#define K_KEY_Z               ::KGE::Key::Z
#define K_KEY_LEFT_BRACKET    ::KGE::Key::LeftBracket   /* [ */
#define K_KEY_BACKSLASH       ::KGE::Key::Backslash     /* \ */
#define K_KEY_RIGHT_BRACKET   ::KGE::Key::RightBracket  /* ] */
#define K_KEY_GRAVE_ACCENT    ::KGE::Key::GraveAccent   /* ` */
#define K_KEY_WORLD_1         ::KGE::Key::World1        /* non-US #1 */
#define K_KEY_WORLD_2         ::KGE::Key::World2        /* non-US #2 */

/* Function keys */
#define K_KEY_ESCAPE          ::KGE::Key::Escape
#define K_KEY_ENTER           ::KGE::Key::Enter
#define K_KEY_TAB             ::KGE::Key::Tab
#define K_KEY_BACKSPACE       ::KGE::Key::Backspace
#define K_KEY_INSERT          ::KGE::Key::Insert
#define K_KEY_DELETE          ::KGE::Key::Delete
#define K_KEY_RIGHT           ::KGE::Key::Right
#define K_KEY_LEFT            ::KGE::Key::Left
#define K_KEY_DOWN            ::KGE::Key::Down
#define K_KEY_UP              ::KGE::Key::Up
#define K_KEY_PAGE_UP         ::KGE::Key::PageUp
#define K_KEY_PAGE_DOWN       ::KGE::Key::PageDown
#define K_KEY_HOME            ::KGE::Key::Home
#define K_KEY_END             ::KGE::Key::End
#define K_KEY_CAPS_LOCK       ::KGE::Key::CapsLock
#define K_KEY_SCROLL_LOCK     ::KGE::Key::ScrollLock
#define K_KEY_NUM_LOCK        ::KGE::Key::NumLock
#define K_KEY_PRINT_SCREEN    ::KGE::Key::PrintScreen
#define K_KEY_PAUSE           ::KGE::Key::Pause
#define K_KEY_F1              ::KGE::Key::F1
#define K_KEY_F2              ::KGE::Key::F2
#define K_KEY_F3              ::KGE::Key::F3
#define K_KEY_F4              ::KGE::Key::F4
#define K_KEY_F5              ::KGE::Key::F5
#define K_KEY_F6              ::KGE::Key::F6
#define K_KEY_F7              ::KGE::Key::F7
#define K_KEY_F8              ::KGE::Key::F8
#define K_KEY_F9              ::KGE::Key::F9
#define K_KEY_F10             ::KGE::Key::F10
#define K_KEY_F11             ::KGE::Key::F11
#define K_KEY_F12             ::KGE::Key::F12
#define K_KEY_F13             ::KGE::Key::F13
#define K_KEY_F14             ::KGE::Key::F14
#define K_KEY_F15             ::KGE::Key::F15
#define K_KEY_F16             ::KGE::Key::F16
#define K_KEY_F17             ::KGE::Key::F17
#define K_KEY_F18             ::KGE::Key::F18
#define K_KEY_F19             ::KGE::Key::F19
#define K_KEY_F20             ::KGE::Key::F20
#define K_KEY_F21             ::KGE::Key::F21
#define K_KEY_F22             ::KGE::Key::F22
#define K_KEY_F23             ::KGE::Key::F23
#define K_KEY_F24             ::KGE::Key::F24
#define K_KEY_F25             ::KGE::Key::F25

/* Keypad */
#define K_KEY_KP_0            ::KGE::Key::KP0
#define K_KEY_KP_1            ::KGE::Key::KP1
#define K_KEY_KP_2            ::KGE::Key::KP2
#define K_KEY_KP_3            ::KGE::Key::KP3
#define K_KEY_KP_4            ::KGE::Key::KP4
#define K_KEY_KP_5            ::KGE::Key::KP5
#define K_KEY_KP_6            ::KGE::Key::KP6
#define K_KEY_KP_7            ::KGE::Key::KP7
#define K_KEY_KP_8            ::KGE::Key::KP8
#define K_KEY_KP_9            ::KGE::Key::KP9
#define K_KEY_KP_DECIMAL      ::KGE::Key::KPDecimal
#define K_KEY_KP_DIVIDE       ::KGE::Key::KPDivide
#define K_KEY_KP_MULTIPLY     ::KGE::Key::KPMultiply
#define K_KEY_KP_SUBTRACT     ::KGE::Key::KPSubtract
#define K_KEY_KP_ADD          ::KGE::Key::KPAdd
#define K_KEY_KP_ENTER        ::KGE::Key::KPEnter
#define K_KEY_KP_EQUAL        ::KGE::Key::KPEqual

#define K_KEY_LEFT_SHIFT      ::KGE::Key::LeftShift
#define K_KEY_LEFT_CONTROL    ::KGE::Key::LeftControl
#define K_KEY_LEFT_ALT        ::KGE::Key::LeftAlt
#define K_KEY_LEFT_SUPER      ::KGE::Key::LeftSuper
#define K_KEY_RIGHT_SHIFT     ::KGE::Key::RightShift
#define K_KEY_RIGHT_CONTROL   ::KGE::Key::RightControl
#define K_KEY_RIGHT_ALT       ::KGE::Key::RightAlt
#define K_KEY_RIGHT_SUPER     ::KGE::Key::RightSuper
#define K_KEY_MENU            ::KGE::Key::Menu
