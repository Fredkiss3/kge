#pragma once
#include "Component.h"
#include "KGE/Events/Event.h"

namespace KGE {

	// Component Category
#define CC(type_) const ComponentCategory GetCategory() const override { \
		return ComponentCategory::type_; \
	} \
	static std::string GetStaticTypeName() { return type<type_>(); } \
	 ~type_() \
	{ \
		K_CORE_ERROR("Deleting component {}", type(*this)); \
	}

	class Behaviour : public Component, public EventListener {
	public:
		virtual void OnUpdate(double ts) {};

		CC(Behaviour);
		CLASS_TYPE(Behaviour);

	protected:
		ComponentCategory m_Type = ComponentCategory::Behaviour;
	};

	// Allow usage of both 'Behaviour & Behavior'
	typedef Behaviour Behavior;

	struct Transform : public Component {
		struct Vec2 {
			double x, y;
		};

		Transform(Vec2 pos = { 0, 0 }, Vec2 scale = {1, 1}, float angle = 0) 
			: pos(pos), scale(scale), angle(angle) {}

		Vec2 pos;
		Vec2 scale;
		float angle;

		CC(Transform);
		CLASS_TYPE(Transform);
	};
}