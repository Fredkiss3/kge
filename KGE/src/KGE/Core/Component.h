//
// Created by Fredkiss3 on 03/07/2020.
//

#pragma once
#include "KGE/Base.h"
#include "headers.h"

namespace KGE
{
	enum class ComponentCategory
	{
		None = 0,
		Transform = 1,
		Behaviour = 2,
		Script = 3,
	};
		class Behaviour;

	class Entity;

	struct Component
	{
	public:
		/*
			* Called when the component is attached to the entity
			*/
		virtual void Init()
		{
			K_CORE_INFO("Initizaling the component {}", type(*this));
		};

		/*
			* Get the category of the component
			*/
		const virtual ComponentCategory GetCategory() const = 0;

		Entity* entity = nullptr;

		/*
		* Return a pointer to the Component if found, otherwise it returns a nullptr
		*/
		Behaviour* GetBehaviour(const std::string& type);
		Component* GetComponent(ComponentCategory category);

		const bool HasBehaviour(const std::string& type) const;
		const bool HasComponent(ComponentCategory category) const;

		/*
		* For Usage in C++ only
		*/
		template <typename T>
		T& GetComponent()
		{
			return castRef<T>(GetComponent(T::GetStaticType));
		}

		bool active = true;

		/*
		* Get real type
		*/
		virtual std::string GetTypeName() { return type(*this); }

		static std::string GetStaticTypeName() { return type<Component>(); }

		static const char* GetStaticType() { return "Component"; }
		virtual const char* GetType() const { return GetStaticType(); }

		virtual ~Component();
	};
} // namespace KGE
