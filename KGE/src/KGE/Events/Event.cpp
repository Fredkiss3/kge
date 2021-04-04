//
// Created by Fredkiss3 on 04/07/2020.
//
#include "headers.h"
#include "KGE/Events/Event.h"
#include "KGE/Core/Scene.h"
#include "KGE/Core/Entity.h"

namespace KGE
{

	Ref<EventQueue> EventQueue::s_Instance = nullptr;

	const std::string Event::Print() const
	{
		std::string str = GetType();

		str += "{ ";
		str += "scene=";

		if (scene != nullptr)
		{
			str += scene->GetName();
		}
		else
		{
			str += "None";
		}

		str += ", Handled=";

		if (handled)
		{
			str += "true";
		}
		else
		{
			str += "false";
		}

		if (entity != nullptr) {
			str += ", entity=";
			str += entity->tag();
		}

		str += ", ";
		str += GetData();
		str += " }";

		return str;
	}

} // namespace KGE
