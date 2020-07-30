#pragma once

#include "headers.h"
#include <glm/glm.hpp>
#include <cmath>
#include "KGE/Base.h"

namespace KGE
{

struct Vec3
{
	Vec3(double xi = 0.0f, double yi = 0.0f, double zi = 0.0f) : x(xi), y(yi), z(zi) {}
	Vec3(Vec3 &other) : Vec3(other.x, other.y, other.z) {}
	Vec3(const Vec3 &other) : Vec3(other.x, other.y, other.z) {}
	Vec3(const Vec3 &&other) : Vec3(other.x, other.y, other.z) {}

	// Construct from glm::vec3 in order to switch between types easily
	Vec3(glm::vec3 &other) : Vec3(other.x, other.y, other.z) {}
	Vec3(const glm::vec3 &other) : Vec3(other.x, other.y, other.z) {}
	Vec3(const glm::vec3 &&other) : Vec3(other.x, other.y, other.z) {}

	// Conversion to glm::vec3 for convenience
	operator glm::vec3() { return {x, y, z}; }
	operator const glm::vec3 &() const { return {x, y, z}; }

	double operator[](size_t index)
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

	double magnitude() const
	{
		return glm::length(glm::vec3(*this));
	}

	double dist(const Vec3 &other)
	{
		return glm::distance(glm::vec3(*this), glm::vec3(other));
	}

	Vec3 lerp(const Vec3 &other, double p)
	{
		auto &self = *this;
		return self + (other - self) * p;
	}

	Vec3 moveTowards(const Vec3 &from, const Vec3 &to, double speed)
	{
		auto v = to - from;
		auto len = v.magnitude();

		if (len <= speed or len == 0)
		{
			return to;
		}
		else
		{
			return from + (v / len) * speed;
		}
	}

	Vec3 &operator=(const Vec3 &other)
	{
		x = other.x;
		y = other.x;
		z = other.z;
	}

	Vec3 &operator=(const Vec3 &&other)
	{
		x = other.x;
		y = other.x;
		z = other.z;
	}

	/*
	 * Return normalized value of this vector (vector of magnitude 1) 
	*/
	Vec3 normalized()
	{
		auto len = magnitude();
		auto &self = *this;

		return len != 0 ? self / len : Vec3(self);
	}

	void normalize()
	{
		*this = normalized();
	}

	Vec3 Up()
	{
		return {0, 1};
	}

	Vec3 Down()
	{
		return {0, -1};
	}

	Vec3 Left()
	{
		return {-1, 0};
	}

	Vec3 Right()
	{
		return {1, 0};
	}

	Vec3 Unit()
	{
		return {1, 1, 1};
	}

	double x, y, z;
};

struct Vec2 : Vec3
{
	Vec2(double xi = 0.0f, double yi = 0.0f) : Vec3(xi, yi)
	{
	}

	Vec2(Vec2 &other) : Vec3(other) {}
	Vec2(const Vec2 &other) : Vec3(other) {}
	Vec2(const Vec2 &&other) : Vec3(other) {}

	Vec2(Vec3 &other) : Vec3(other) {}
	Vec2(const Vec3 &other) : Vec3(other) {}
	Vec2(const Vec3 &&other) : Vec3(other) {}

	// Conversion to glm::vec3 for convenience
	operator Vec3() { return {x, y, z}; }
	operator const Vec3 &() const { return {x, y, z}; }

	Vec2 &operator=(const Vec2 &other)
	{
		x = other.x;
		y = other.x;
	}

	Vec2 &operator=(const Vec2 &&other)
	{
		x = other.x;
		y = other.x;
	}

	double operator[](size_t index)
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

	double angleTo(const Vec2 &other) const
	{
		auto &self = *this;
		auto cross = self.x * other.x - self.y * other.y;
		auto dot = self.x * other.x + self.y * other.y;
		return glm::degrees(atan2(cross, dot));
	}

	double angle() const
	{
		return magnitude() == 0 ? 0 : glm::degrees(atan2(y, x));
	}

	Vec2 rotated(float angle) const
	{
		auto &self = *this;
		auto rad = glm::radians(angle);
		auto cos = glm::cos(rad);
		auto sin = glm::sin(rad);

		auto xi = self.x * cos - self.y * sin;
		auto yi = self.x * sin + self.y * cos;
		return {xi, yi};
	}

	void rotate(float angle)
	{
		*this = rotated(angle);
	}

	operator glm::vec2() { return {x, y}; }
	operator const glm::vec2 &() const { return {x, y}; }

private:
	double z;
};

// Print
std::ostream &operator<<(std::ostream &out, const Vec2 &v)
{
	return out << "(" << v.x << ", " << v.y << ")";
}

std::ostream &operator<<(std::ostream &out, const Vec3 &v)
{
	return out << "(" << v.x << ", " << v.y << ", " << v.z << ")";
}

// Operators
Vec3
operator*(const Vec3 &v1, const Vec3 &v2)
{
	return glm::vec3(v1) * glm::vec3(v2);
}

Vec3 operator*(double scalar, const Vec3 &v)
{
	return {v.x * scalar, v.y * scalar, v.z * scalar};
}

Vec3 operator*(const Vec3 &v1, const Vec3 &v2)
{
	return glm::vec3(v1) * glm::vec3(v2);
}

Vec3 operator/(const Vec3 &v, double scalar)
{
	return {v.x / scalar, v.y / scalar, v.z / scalar};
}

Vec3 operator+(const Vec3 &v1, const Vec3 &v2)
{
	return glm::vec3(v1) + glm::vec3(v2);
}

Vec3 operator-(const Vec3 &v1, const Vec3 &v2)
{
	return glm::vec3(v1) - glm::vec3(v2);
}

Vec3 operator-(const Vec3 &v)
{
	return {-v.x, -v.y, -v.z};
}

bool operator>(const Vec3 &v1, const Vec3 &v2)
{
	return v1.magnitude() > v2.magnitude();
}

bool operator>=(const Vec3 &v1, const Vec3 &v2)
{
	return v1.magnitude() >= v2.magnitude();
}

bool operator<(const Vec3 &v1, const Vec3 &v2)
{
	return v1.magnitude() < v2.magnitude();
}

bool operator<=(const Vec3 &v1, const Vec3 &v2)
{
	return v1.magnitude() <= v2.magnitude();
}

} // namespace KGE
