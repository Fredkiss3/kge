//
// Created by Fredkiss3 on 04/07/2020.
//

#pragma once
#include "headers.h"
#include "KGE/Base.h"
#include "KGE/Events/Event.h"
#include "KGE/Utils/Log.h"

namespace KGE
{

	/*
	* A component Manager is a class that holds components
	* */
	class ComponentManager : public EventListener
	{
	public:
		ComponentManager(bool debugPrint = true): EventListener(debugPrint) {}
		TYPE_NAME
	};

} // namespace KGE
