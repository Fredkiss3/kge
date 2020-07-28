#pragma once
#include "KGE/Core/ComponentManager.h"
#include "Window.h"

namespace KGE {
	class Renderer : public ComponentManager
	{
	public:
		void OnInit() override;

		void OnUpdate();
		void OnPreUpdate();
		Renderer();

	public:
		static Scope<Window>& GetWindow()
		{
			return s_Window;
		}
	private:
		static Scope<Window> s_Window;
	};
}
