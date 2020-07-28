#pragma once
#include "KGE/Events/Events.h"

namespace KGE {

	struct DrawGizMos : public Event
	{
		CLASS_TYPE(DrawGizMos);
	};

	struct ImGuiDraw : public Event
	{
		CLASS_TYPE(ImGuiDraw);
	};

}