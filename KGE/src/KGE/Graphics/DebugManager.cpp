#include "headers.h"
#include "DebugManager.h"
#include "KGE/Engine.h"
#include "Renderer.h"

#include <imgui.h>
#include <examples/imgui_impl_glfw.h>
#include <examples/imgui_impl_opengl3.h>
#include <GLFW/glfw3.h>
#include <glad/glad.h>

namespace KGE {
	DebugManager::DebugManager(): ComponentManager(false)
	{
		Bind<DrawGizMos>(K_BIND_EVENT_FN(DebugManager::OnDrawGizMos));
		Bind<ImGuiDraw>(K_BIND_EVENT_FN(DebugManager::OnImguiDraw));
		Bind<KeyPressed>(K_BIND_EVENT_FN(DebugManager::OnKeyPressed));
		Bind<KeyReleased>(K_BIND_EVENT_FN(DebugManager::OnKeyReleased));
		Bind<MouseReleased>(K_BIND_EVENT_FN(DebugManager::OnMouseReleased));
		Bind<MousePressed>(K_BIND_EVENT_FN(DebugManager::OnMousePressed));
		Bind<MouseMoved>(K_BIND_EVENT_FN(DebugManager::OnMouseMoved));
		Bind<MouseScrolled>(K_BIND_EVENT_FN(DebugManager::OnMouseScrolled));
	}


	void DebugManager::OnInit()
	{
		// Setup Dear ImGui:: context
		IMGUI_CHECKVERSION();
		ImGui::CreateContext();
		ImGuiIO& io = ImGui::GetIO(); (void)io;
		io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;       // Enable Keyboard Controls
		//io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;      // Enable Gamepad Controls
		io.ConfigFlags |= ImGuiConfigFlags_DockingEnable;           // Enable Docking
		io.ConfigFlags |= ImGuiConfigFlags_ViewportsEnable;         // Enable Multi-Viewport / Platform Windows
		//io.ConfigFlags |= ImGuiConfigFlags_ViewportsNoTaskBarIcons;
		//io.ConfigFlags |= ImGuiConfigFlags_ViewportsNoMerge;

		// Setup Dear ImGui:: style
		ImGui::StyleColorsDark();
		//ImGui::StyleColorsClassic();

		// When viewports are enabled we tweak WindowRounding/WindowBg so platform windows can look identical to regular ones.
		ImGuiStyle& style = ImGui::GetStyle();
		if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable)
		{
			style.WindowRounding = 0.0f;
			style.Colors[ImGuiCol_WindowBg].w = 1.0f;
		}

		GLFWwindow* window = Renderer::GetWindow()->GetNativeWindow();

		// Setup Platform/Renderer bindings
		ImGui_ImplGlfw_InitForOpenGL(window, true);
		ImGui_ImplOpenGL3_Init("#version 410");
	}

	void DebugManager::OnKeyPressed(KeyPressed& e)
	{
		BlockEvents(e);
	}

	void DebugManager::OnKeyReleased(KeyReleased& e)
	{
		BlockEvents(e);
	}

	void DebugManager::OnMouseReleased(MouseReleased& e)
	{
		BlockEvents(e);
	}

	void DebugManager::OnMousePressed(MousePressed& e)
	{
		BlockEvents(e);
	}

	void DebugManager::OnMouseMoved(MouseMoved& e)
	{
		BlockEvents(e);
	}

	void DebugManager::OnMouseScrolled(MouseScrolled& e)
	{
		BlockEvents(e);
	}

	void DebugManager::OnDestroy()
	{
		ImGui_ImplOpenGL3_Shutdown();
		ImGui_ImplGlfw_Shutdown();
		ImGui::DestroyContext();
	}

	void DebugManager::OnDrawGizMos(DrawGizMos& e)
	{
		// TODO : After Renderer Has been finished
		auto& scene = Engine::GetInstance()->GetCurrentScene();

		if (scene) {
			scene->Reg().view<ScriptComponent>().each([&](auto entity, ScriptComponent& script)
				{
					if (e.handled) return;
					script.OnEvent(e);
				}
			);
		}

		e.handled = true;
	}

	void DebugManager::OnImguiDraw(ImGuiDraw& e)
	{
		auto& scene = Engine::GetInstance()->GetCurrentScene();

		// Begin ImGui::
		BeginFrame();

		if (scene) {
			scene->Reg().view<ScriptComponent>().each([&](auto entity, ScriptComponent& script)
				{
					if (e.handled) return;
					script.OnEvent(e);
				}
			);
		}

		// End ImGui::
		EndFrame();

		e.handled = true;
	}
	void DebugManager::BeginFrame()
	{
		ImGui_ImplOpenGL3_NewFrame();
		ImGui_ImplGlfw_NewFrame();
		ImGui::NewFrame();

		// Display Hardware Infos
		ImGui::PushStyleVar(ImGuiStyleVar_WindowRounding, 5.0f);
		ImGui::PushStyleVar(ImGuiStyleVar_WindowBorderSize, 0.0f);
		ImGui::SetNextWindowSize(ImVec2{ 330.0f, 70.0f });

		auto flags = ImGuiWindowFlags_NoTitleBar |
			ImGuiWindowFlags_NoCollapse |
			ImGuiWindowFlags_NoResize |
			ImGuiWindowFlags_NoFocusOnAppearing;

		ImGui::Begin("HARDWARE Infos", false, flags);
		ImGui::Text("OpenGL Vendor: %s", glGetString(GL_VENDOR));
		ImGui::Text("OpenGL Version %s", glGetString(GL_VERSION));
		ImGui::Text("OpenGL Renderer: %s", glGetString(GL_RENDERER));
		ImGui::PopStyleVar();
		ImGui::PopStyleVar();
		ImGui::End();

		// Show the Demo Window
		ImGui::ShowDemoWindow();
	}

	void DebugManager::EndFrame()
	{
		ImGuiIO& io = ImGui::GetIO();
		io.DisplaySize = ImVec2((float)Renderer::GetWindow()->GetWidth(), (float)Renderer::GetWindow()->GetHeight());

		// Rendering
		ImGui::Render();
		ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

		if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable)
		{
			GLFWwindow* backup_current_context = glfwGetCurrentContext();
			ImGui::UpdatePlatformWindows();
			ImGui::RenderPlatformWindowsDefault();
			glfwMakeContextCurrent(backup_current_context);
		}
	}
	void DebugManager::BlockEvents(Event& e)
	{
		ImGuiIO& io = ImGui::GetIO();
		e.handled |= io.WantCaptureMouse;
		e.handled |= io.WantCaptureKeyboard;
		e.handled = true;
	}
}