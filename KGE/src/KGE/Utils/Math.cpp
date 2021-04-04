#include "headers.h"
#include "Math.h"

namespace KGE {
	/*
	* Return normalized value of this vector (vector of magnitude 1)
	*/
	Vec3  Vec3::normalized() const
	{
		auto len = magnitude();
		auto& self = *this;

		return len != 0 ? self / len : Vec3(self);
	}

	Vec3 Vec3::lerp(const Vec3& other, float p) const
	{
		auto& self = *this;
		return self + (other - self) * p;
	}

	Vec3 Vec3::MoveTowards(const Vec3& from, const Vec3& to, float speed)
	{
		auto v = to - from;
		float len = v.magnitude();

		if (len <= speed || len == 0)
		{
			return to;
		}
		else
		{
			return from + (v/len) * speed;
		}
	}

	float Vec2::angleTo(const Vec2& other) const
	{
		auto& self = *this;
		auto cross = self.x * other.x - self.y * other.y;
		auto dot = self.x * other.x + self.y * other.y;
		return glm::degrees(atan2(cross, dot));
	}

	float Vec2::angle() const
	{
		return magnitude() == 0 ? 0 : glm::degrees(atan2(y, x));
	}

	Vec2 Vec2::rotated(float angle) const
	{
		auto& self = *this;
		auto rad = glm::radians(angle);
		auto cos = glm::cos(rad);
		auto sin = glm::sin(rad);

		auto xi = self.x * cos - self.y * sin;
		auto yi = self.x * sin + self.y * cos;
		return { xi, yi };
	}

	std::ostream& operator<<(std::ostream& out, const Vec2& v)
	{
		return out << "Vec2(" << v.x << ", " << v.y << ")";
	}

	std::ostream& operator<<(std::ostream& out, const Vec3& v)
	{
		return out << "Vec3(" << v.x << ", " << v.y << ", " << v.z << ")";
	}


}