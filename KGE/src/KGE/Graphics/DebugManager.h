#pragma once
#include "KGE/Core/ComponentManager.h"
#include "Events.h"
#include "KGE/Inputs/KeyEvents.h"
#include "KGE/Inputs/MouseEvents.h"

namespace KGE {
	class DebugManager : public ComponentManager
	{
	public:
		DebugManager();

		void OnInit() override;
		
		void OnKeyPressed(KeyPressed& e);
		void OnKeyReleased(KeyReleased& e);
		void OnMouseReleased(MouseReleased& e);
		void OnMousePressed(MousePressed& e);
		void OnMouseMoved(MouseMoved& e);
		void OnMouseScrolled(MouseScrolled& e);

		void OnDestroy() override;
		void OnDrawGizMos(DrawGizMos& e);
		void OnImguiDraw(ImGuiDraw& e);

	private:
		void BeginFrame();
		void EndFrame();
		void BlockEvents(Event& e);
	};
}
