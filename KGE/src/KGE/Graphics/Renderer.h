#pragma once
#include "KGE/Core/ComponentManager.h"
#include "Window.h"

namespace KGE {
		


	class Renderer : public ComponentManager
	{
	public:
		//Renderer();
		~Renderer();

		void OnStartScene(StartScene& ev);

		void OnWindowResize(WindowResize& ev);
		void OnInit() override;

		void OnPostRender();
		void OnPreRender();
		Renderer(const WindowProps& props = {});
		void OnRender();

	public:
		static Scope<Window>& GetWindow()
		{
			return s_Window;
		}
	private:
		WindowProps m_WindowProps;
		
		void Setup();

	private:
		static Scope<Window> s_Window;
		
	};
}
