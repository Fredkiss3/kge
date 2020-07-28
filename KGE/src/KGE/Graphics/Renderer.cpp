#include "headers.h"
#include "Renderer.h"
#include "KGE/Engine.h"
#include <glad/glad.h>

namespace KGE {
	Scope<Window> Renderer::s_Window = nullptr;

	void Renderer::OnInit()
	{
		K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before to initialize renderer");

		auto& name = Engine::GetInstance()->GetApplicationName();
		s_Window = Window::Create(WindowProps(name));

		// Dump OpenGL Infos
		K_CORE_INFO("OpenGL Info:");
		K_CORE_INFO("  Vendor: {0}", glGetString(GL_VENDOR));
		K_CORE_INFO("  Renderer: {0}", glGetString(GL_RENDERER));
		K_CORE_INFO("  Version: {0}", glGetString(GL_VERSION));

		// Should use OpenGL at least version 4.4.0
		int versionMajor;
		int versionMinor;
		glGetIntegerv(GL_MAJOR_VERSION, &versionMajor);
		glGetIntegerv(GL_MINOR_VERSION, &versionMinor);
		K_CORE_ASSERT(versionMajor > 4 || (versionMajor == 4 && versionMinor >= 4), "KGE requires at least OpenGL version 4.4!");
	}

	void Renderer::OnUpdate()
	{
		s_Window->OnUpdate();
	}

	void Renderer::OnPreUpdate()
	{
		// Clear Screen Before Update
		glClearColor(0, 0, 0, 0);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	}

	Renderer::Renderer()
	{

	}
}