#pragma once

#include "headers.h"
#include <glm/glm.hpp>
#include "KGE/Base.h"

namespace KGE
{

	struct Vec3
	{
		Vec3(float xi = 0.0f, float yi = 0.0f, float zi = 0.0f) : x(xi), y(yi), z(zi) {}
		Vec3(Vec3& other) : Vec3(other.x, other.y, other.z) {}
		Vec3(const Vec3& other) : Vec3(other.x, other.y, other.z) {}
		Vec3(const Vec3&& other) : Vec3(other.x, other.y, other.z) {}

		// Construct from glm::vec3 in order to switch between types easily
		Vec3(glm::vec3& other) : Vec3(other.x, other.y, other.z) {}
		Vec3(const glm::vec3& other) : Vec3(other.x, other.y, other.z) {}
		Vec3(const glm::vec3&& other) : Vec3(other.x, other.y, other.z) {}

		// Conversion to glm::vec3 for convenience
		operator glm::vec3() const& { return glm::vec3{ x, y, z }; }
	/*	operator float*() const& { 
			float tab[] = { x, y, z };
			return tab; 
		}*/
		operator const glm::vec3& () const { return glm::vec3{ x, y, z }; }

		float operator[](size_t index)
		{
			K_CORE_ASSERT(index >= 0 && index <= 2, "The index of the Vec3 should be between 0 & 2");

			switch (index)
			{
			default:
			case 0:
				return x;
			case 1:
				return y;
			case 2:
				return z;
			}
		}

		float magnitude() const
		{
			return glm::length(glm::vec3(*this));
		}

		float dist(const Vec3& other) const
		{
			auto& self = *this;
			return glm::distance(glm::vec3(self), glm::vec3(other));
		}


		void operator=(const Vec3& other)
		{
			x = other.x;
			y = other.y;
			z = other.z;
		}

		void operator=(const Vec3&& other) noexcept
		{
			x = other.x;
			y = other.y;
			z = other.z;
		}

		/*
		 * Return normalized value of this vector (vector of magnitude 1)
		*/
		Vec3 normalized() const;

		Vec3 lerp(const Vec3& other, float p) const;

		static Vec3 MoveTowards(const Vec3& from, const Vec3& to, float speed);


		void normalize()
		{
			*this = normalized();
		}

		static Vec3 Up()
		{
			return Vec3{ 0.0f, 1.0f, 0.0f };
		}

		static Vec3 Zero() 
		{
			return Vec3{ 0.0f, 0.0f, 0.0f };
		}

		static Vec3 Down() 
		{
			return Vec3{ 0.0f, -1.0f, 0.0f };
		}

		static Vec3 Left()
		{
			return Vec3{ -1.0f, 0.0f, 0.0f };
		}

		static Vec3 Right() 
		{
			return Vec3{ 1.0f, 0.0f, 0.0f };
		}

		static Vec3 Unit() 
		{
			return Vec3{ 1.0f, 1.0f, 1.0f };
		}


	/*	inline void operator+=(const Vec3& v2)
		{
			*this = glm::vec3(*this) + glm::vec3(v2);
		}

		inline void operator-=(const Vec3& v2)
		{
			*this = glm::vec3(*this) - glm::vec3(v2);
		}*/

		float x, y, z;
	};

	struct Vec2 : Vec3
	{
		Vec2(float xi = 0.0f, float yi = 0.0f) : Vec3(xi, yi)
		{
		}

		Vec2(Vec2& other) : Vec3(other) {}
		Vec2(const Vec2& other) : Vec3(other) {}
		Vec2(const Vec2&& other) : Vec3(other) {}

		Vec2(Vec3& other) : Vec3(other) {}
		Vec2(const Vec3& other) : Vec3(other) {}
		Vec2(const Vec3&& other) : Vec3(other) {}

		// Conversion to glm::vec3 for convenience
		operator Vec3() { return { x, y, z }; }
		operator const Vec3& () const { return { x, y, z }; }

		void operator=(const Vec2& other)
		{
			x = other.x;
			y = other.y;
		}

		void operator=(const Vec2&& other)
		{
			x = other.x;
			y = other.y;
		}

		float operator[](size_t index)
		{
			K_CORE_ASSERT(index >= 0 && index <= 1, "The index of the Vec2 should be between 0 & 1");

			switch (index)
			{
			default:
			case 0:
				return x;
			case 1:
				return y;
			}
		}

		float angleTo(const Vec2& other) const;

		float angle() const;

		Vec2 rotated(float angle) const;

		void rotate(float angle)
		{
			*this = rotated(angle);
		}

		operator glm::vec2() { return { x, y }; }
		operator const glm::vec2& () const { return { x, y }; }

	private:
		float z = 0;
	};

	// Print
	std::ostream& operator<<(std::ostream& out, const Vec2& v);

	std::ostream& operator<<(std::ostream& out, const Vec3& v);

	// Operators
	inline Vec3 operator*(const Vec3& v, float scalar)
	{
		return { v.x * scalar, v.y * scalar, v.z * scalar };
	}

	inline Vec3 operator*(const Vec3& v, int scalar)
	{
		return { v.x * scalar, v.y * scalar, v.z * scalar };
	}

	inline Vec3 operator*(const Vec3& v, double scalar)
	{
		return { v.x *  (float) scalar, v.y * (float) scalar, v.z * (float) scalar };
	}

	inline Vec3 operator*(const float scalar, const Vec3& v)
	{
		return { v.x * scalar, v.y * scalar, v.z * scalar };
	}

	inline Vec3 operator*(const int scalar, const Vec3& v)
	{
		return { v.x * scalar, v.y * scalar, v.z * scalar };
	}

	inline Vec3 operator*(const Vec3& v1, const Vec3& v2)
	{
		return glm::vec3(v1) * glm::vec3(v2);
	}

	

	
	inline Vec3 operator/(const Vec3& v, float scalar)
	{
		return { v.x / scalar, v.y / scalar, v.z / scalar };
	}

	/*inline Vec3 operator/(const Vec3& v, double scalar)
	{
		return v / (float)scalar;
	}

	inline Vec3 operator/(const Vec3& v, int scalar)
	{
		return v / (float)scalar;
	}*/

	inline Vec3 operator+(const Vec3& v1, const Vec3& v2)
	{
		return glm::vec3(v1) + glm::vec3(v2);
	}

	inline Vec3 operator-(const Vec3& v1, const Vec3& v2)
	{
		return glm::vec3(v1) - glm::vec3(v2);
	}


	inline Vec3 operator-(const Vec3& v)
	{
		return { -v.x, -v.y, -v.z };
	}

	inline bool operator>(const Vec3& v1, const Vec3& v2)
	{
		return v1.magnitude() > v2.magnitude();
	}

	inline bool operator>=(const Vec3& v1, const Vec3& v2)
	{
		return v1.magnitude() >= v2.magnitude();
	}

	inline bool operator<(const Vec3& v1, const Vec3& v2)
	{
		return v1.magnitude() < v2.magnitude();
	}

	inline bool operator<=(const Vec3& v1, const Vec3& v2)
	{
		return v1.magnitude() <= v2.magnitude();
	}

	inline bool operator==(const Vec3& v1, const Vec3& v2)
	{
		return v1.x == v2.x && v1.y == v2.y && v1.z == v2.z ;
	}

	inline bool operator==(const Vec2& v1, const Vec2& v2)
	{
		return v1.x == v2.x && v1.y == v2.y;
	}

} // namespace KGE
