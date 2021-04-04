#pragma once
#include "Component.h"
#include "KGE/Events/Events.h"
#include "KGE/Utils/Math.h"
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>

namespace KGE
{

// Component Category
#define CC(type_) \
	const ComponentCategory GetCategory() const override { return ComponentCategory::type_; } \
	static const ComponentCategory GetStaticCategory() { return ComponentCategory::type_; }

struct Behaviour : public EventListener
{
public:
	virtual void OnUpdate(double ts){};

	~Behaviour() = default;
	Behaviour() = default;
	
	//{
	//	//K_CORE_ERROR("Deleting A Behaviour");
	//}

	friend struct ScriptComponent;
	Entity* entity;
	//CC(Behaviour);
};

// Allow usage of both 'Behaviour & Behavior'
typedef Behaviour Behavior;

/*
	* A Script can have multiple behaviours attached
	*/
struct ScriptComponent : public Component
{
public:
	operator Behavior& ()
	{
		return *behaviour;
	}

	ScriptComponent(Behaviour* bh): behaviour(bh)
	{
		behaviour->entity = entity;
	};

	template<typename T, typename... Args>
	void Attach(Args&&... args)
	{
		behaviour = Ref<Behavior>(new T(std::forward<Args>(args)...));
		behaviour->entity = entity;
	}

	void Detach() {
		behaviour->entity = nullptr;
		behaviour = nullptr;
	}

	void Attach(Behavior* bh) {
		behaviour = Ref<Behavior>(bh);
		behaviour->entity = entity;
	}

	ScriptComponent() 
	{
		behaviour = nullptr;
	};

	void OnInit()
	{
		if (behaviour) behaviour->OnInit();
	}

	void OnEvent(Event &e)
	{
		if (behaviour) behaviour->OnEvent(e);
	}

	void OnUpdate(double ts)
	{
		if(behaviour) behaviour->OnUpdate(ts);
	}

	~ScriptComponent()
	{
	}

	CC(Script);
	CLASS_TYPE(ScriptComponent);

public:
	Ref<Behaviour> behaviour;
};


struct TagComponent : public Component
{
	std::string tag;

	//TagComponent() = default;
	//TagComponent(const TagComponent&) = default;
	TagComponent(const std::string& tag = "")
		: tag(tag) {}

	CC(Tag);
	CLASS_TYPE(TagComponent);
};


struct TransformComponent : public Component
{

	TransformComponent(Vec3 _pos = Vec3::Zero(), Vec3 _scale = Vec3::Unit(), Vec3 _angle = Vec3::Zero())
		: pos(_pos), scale(_scale), rotation(_angle) {}

	/*TransformComponent(const TransformComponent& other)
	 : pos(other.pos), scale(other.scale), rotation(other.rotation) {}*/



	operator glm::mat4() 
	{ 
		auto angle = glm::rotate(glm::mat4(1.0f), rotation.x, { 1, 0, 0 })
			* glm::rotate(glm::mat4(1.0f), rotation.y, { 0, 1, 0 })
			* glm::rotate(glm::mat4(1.0f), rotation.z, { 0, 0, 1 });
		return glm::translate(glm::mat4(1), (glm::vec3)pos)
				* angle
				* glm::scale(glm::mat4(1.0), (glm::vec3) scale);
	}

	operator const glm::mat4& () const 
	{ 
		auto angle = glm::rotate(glm::mat4(1.0f), rotation.x, { 1, 0, 0 })
			* glm::rotate(glm::mat4(1.0f), rotation.y, { 0, 1, 0 })
			* glm::rotate(glm::mat4(1.0f), rotation.z, { 0, 0, 1 });
		return glm::translate(glm::mat4(1), (glm::vec3)pos)
			* angle
			* glm::scale(glm::mat4(1.0), (glm::vec3) scale);
	}

	~TransformComponent()
	{
		//K_CORE_ERROR("Deleting Transform Component");
	}


	Vec3 pos;
	Vec3 scale;
	Vec3 rotation;
	CC(Transform);
	CLASS_TYPE(TransformComponent);
};
} // namespace KGE