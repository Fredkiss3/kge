#pragma once
#include "headers.h"
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>

namespace KGE {
	struct Color
	{
		Color(float r_ = 1, float g_ = 1, float b_ = 1, float a_ = 1) : r(r_), g(g_), b(b_), a(a_) {}
		Color() : Color(1) {}

		operator glm::vec4() const& { return glm::vec4{ r, g, b, a }; }
		operator const glm::vec4& () const { return glm::vec4{ r, g, b, a }; }

		float r = 1, g = 1, b = 1, a = 1;


		static Color White()
		{
			return Color{ 1.0f };
		}

		static Color Black()
		{
			return Color{ 0.0f };
		}

		static Color Red() 
		{
			return Color{ 1.0f, 0.0f, 0.0f, 1.0f };
		}

		static Color Blue() 
		{
			return Color{ 0.0f, 1.0f, 0.0f, 1.0f };
		}

		static Color Green() 
		{
			return Color{ 0.0f, 0.0f, 1.0f, 1.0f };
		}

	};
}