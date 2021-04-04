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
		Camera = 4,
		Sprite = 5,
		Tag = 6,
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
		static const ComponentCategory GetStaticCategory() 
		{
			return ComponentCategory::None;
		}

		Entity* entity = nullptr;

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
