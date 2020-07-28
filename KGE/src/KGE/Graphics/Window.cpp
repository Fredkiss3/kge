#include "headers.h"
#include "Window.h"
#include "KGE/Events/Events.h"
#include "KGE/Inputs/KeyEvents.h"
#include "KGE/Inputs/MouseEvents.h"

#include <glad/glad.h>

namespace KGE {
	static bool s_GLFWInitialized = false;

	Scope<Window> KGE::Window::Create(const WindowProps& props)
	{
#ifdef K_PLATFORM_WINDOWS
		return CreateScope<Window>(props);
#else
		K_CORE_ASSERT(false, "Unknown platform!");
		return nullptr;
#endif
	}

	static void GLFWErrorCallback(int error, const char* description)
	{
		K_CORE_ERROR("GLFW Error ({0}): {1}", error, description);
	}

	Window::Window(const WindowProps& props)
	{
		Init(props);
	}

	Window::~Window()
	{
		Shutdown();
	}

	void Window::Init(const WindowProps& props)
	{
		m_Data.Title = props.Title;
		m_Data.Width = props.Width;
		m_Data.Height = props.Height;

		K_CORE_INFO("Creating window {0} ({1}, {2})", props.Title, props.Width, props.Height);

		if (!s_GLFWInitialized)
		{
			int success = glfwInit();
			K_CORE_ASSERT(success, "Could not intialize GLFW!");
			glfwSetErrorCallback(GLFWErrorCallback);
			s_GLFWInitialized = true;
		}
		
		// Create Window & Context
		m_Window = glfwCreateWindow((int)props.Width, (int)props.Height, m_Data.Title.c_str(), nullptr, nullptr);
		glfwMakeContextCurrent(m_Window);

		// Initialze Glad
		int status = gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);
		K_CORE_ASSERT(status, "Failed to initialize Glad!");

		// Set User Pointer
		glfwSetWindowUserPointer(m_Window, &m_Data);
		SetVSync(true);


		// Event Callbacks
		glfwSetWindowSizeCallback(m_Window, [](GLFWwindow* window, int width, int height)
			{
				WindowData& data = *(WindowData*)glfwGetWindowUserPointer(window);

				data.Width = width;
				data.Height = height;

				EventQueue::Dispatch(new WindowResize{ width, height });
			}
		);

		glfwSetWindowCloseCallback(m_Window, [](GLFWwindow* window)
			{
				EventQueue::Dispatch(new Quit);
			}
		);

		glfwSetKeyCallback(m_Window, [](GLFWwindow* window, int key, int scancode, int action, int mods)
			{
				WindowData& data = *(WindowData*)glfwGetWindowUserPointer(window);

				switch (action)
				{
				case GLFW_PRESS:
					EventQueue::Dispatch(new KeyPressed{ static_cast<KeyCode>(key), 0, mods });
					break;
				case GLFW_RELEASE:
					EventQueue::Dispatch(new KeyReleased{ static_cast<KeyCode>(key), mods });
					break;
				case GLFW_REPEAT:
					EventQueue::Dispatch(new KeyPressed{ static_cast<KeyCode>(key), 1, mods });
					break;
				}
			}
		);

		glfwSetMouseButtonCallback(m_Window, [](GLFWwindow* window, int button, int action, int mods)
			{
				WindowData& data = *(WindowData*)glfwGetWindowUserPointer(window);

				switch (action)
				{
				case GLFW_PRESS:
				{
					EventQueue::Dispatch(new MousePressed{ static_cast<MouseCode>(button), mods });
					break;
				}
				case GLFW_RELEASE:
				{
					EventQueue::Dispatch(new MouseReleased{ static_cast<MouseCode>(button), mods });
					break;
				}
				}
			}
		);

		glfwSetScrollCallback(m_Window, [](GLFWwindow* window, double xoffset, double yoffset)
			{
				WindowData& data = *(WindowData*)glfwGetWindowUserPointer(window);
				EventQueue::Dispatch(new MouseScrolled{ xoffset, yoffset });
			}
		);

		glfwSetCursorPosCallback(m_Window, [](GLFWwindow* window, double xPos, double yPos)
			{
				WindowData& data = *(WindowData*)glfwGetWindowUserPointer(window);
				EventQueue::Dispatch(new MouseMoved{ xPos, yPos });
			}
		);
	}

	void Window::Shutdown()
	{
		glfwDestroyWindow(m_Window);
		glfwTerminate();
	}

	void Window::OnUpdate()
	{
		glfwPollEvents();
		glfwSwapBuffers(m_Window);
	}

	void Window::SetVSync(bool enabled)
	{
		if (enabled)
			glfwSwapInterval(1);
		else
			glfwSwapInterval(0);

		m_Data.VSync = enabled;
	}

	bool Window::IsVSync() const
	{
		return m_Data.VSync;
	}

}
