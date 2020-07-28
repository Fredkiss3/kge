#pragma once
#include "headers.h"
#include <glad/glad.h>
#include "KGE/Events/Events.h"

#include <GLFW/glfw3.h>

namespace KGE {

	struct WindowProps
	{
		std::string Title;
		uint32_t Width;
		uint32_t Height;

		WindowProps(const std::string& title = "Kiss Game Engine",
			uint32_t width = 1280,
			uint32_t height = 720)
			: Title(title), Width(width), Height(height)
		{
		}
	};


	class Window {
	private:
		struct WindowData
		{
			std::string Title;
			unsigned int Width, Height;
			bool VSync;

			//EventCallbackFn EventCallback;
		};

		WindowData m_Data;

	public:
		//using EventCallbackFn = std::function<void(Event&)>;

		Window(const WindowProps& props);
		virtual ~Window();

		void OnUpdate();

		unsigned int GetWidth() const  { return m_Data.Width; }
		unsigned int GetHeight() const  { return m_Data.Height; }

		// Window attributes
		/*void SetEventCallback(const EventCallbackFn& callback)
		{ 
			m_Data.EventCallback = callback; 
		}*/
		
		const WindowData& getData() const { return m_Data; }

		void SetVSync(bool enabled);
		bool IsVSync() const;

		GLFWwindow* GetNativeWindow()
		{
			return m_Window;
		}

		static Scope<Window> Create(const WindowProps& props = WindowProps());
	private:
		virtual void Init(const WindowProps& props);
		virtual void Shutdown();

	private:
		// Window Data
		GLFWwindow* m_Window;
	};

}