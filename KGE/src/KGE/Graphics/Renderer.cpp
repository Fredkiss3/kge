#include "headers.h"
#include "Renderer.h"
#include "KGE/Engine.h"
#include <glad/glad.h>
#include <glm/glm.hpp>
#include "LowLevel/Shader.h"
#include "LowLevel/Buffer.h"
#include "LowLevel/VertexArray.h"
#include "LowLevel/RenderAPI.h"
#include "LowLevel/Texture.h"
#include "Components.h"
#include "KGE/Core/Scene.h"

#include "stb_image.h"

namespace KGE {

	Scope<Window> Renderer::s_Window = nullptr;

	void OpenGLLogMessage(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar* message, const void* userParam)
	{
#ifdef K_DEBUG
		switch (severity)
		{
		case GL_DEBUG_SEVERITY_HIGH:
			K_CORE_ERROR("[OpenGL] {0}", message);
			K_CORE_ASSERT(false, "GL_DEBUG_SEVERITY_HIGH");
			break;
		case GL_DEBUG_SEVERITY_MEDIUM:
			K_CORE_WARN("[OpenGL] {0}", message);
			break;
		case GL_DEBUG_SEVERITY_LOW:
			K_CORE_INFO("[OpenGL] {0}", message);
			break;
		case GL_DEBUG_SEVERITY_NOTIFICATION:
			K_CORE_TRACE("[OpenGL] {0}", message);
			break;
		}
#endif // K_DEBUG
	}


	Renderer::Renderer(const WindowProps& props) : m_WindowProps(props)
	{
		Bind<WindowResize>(K_BIND_EVENT_FN(Renderer::OnWindowResize));
		Bind<StartScene>(K_BIND_EVENT_FN(Renderer::OnStartScene));
	}

	Renderer::~Renderer()
	{
		RenderAPI::ShutDown();
	}

	void Renderer::OnStartScene(StartScene& ev)
	{
		K_CORE_WARN("Starting scene for Renderer...");
	}


	void Renderer::OnWindowResize(WindowResize& ev)
	{
		// Resize our non-FixedAspectRatio cameras
		auto& scene = Engine::GetInstance()->GetCurrentScene();
		if (scene) {
			auto view = scene->Reg().view<CameraComponent>();
			for (auto entity : view)
			{
				auto& cameraComponent = view.get<CameraComponent>(entity);
				if (!cameraComponent.FixedAspectRatio)
					cameraComponent.SetViewportSize(s_Window->GetWidth(), s_Window->GetHeight());
			}
		}

	}

	void  Renderer::Setup()
	{
		RenderAPI::Init();
	}

	void Renderer::OnInit()
	{
		K_CORE_ASSERT(Engine::GetStaticInstance(), "Engine should be started before to initialize renderer");

		// Application Name
		auto& name = Engine::GetInstance()->GetApplicationName();
		s_Window = Window::Create(m_WindowProps);

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

		Setup();
	}

	void Renderer::OnPostRender()
	{
		// render 
		s_Window->OnUpdate();
	}

	void Renderer::OnPreRender()
	{
		// Clear Screen Before Update
		glViewport(0, 0, s_Window->GetWidth(), s_Window->GetHeight());

		float color[] = { 0.1f, 0.1f, 0.1f, 1.0f };

		auto& scene = Engine::GetInstance()->GetCurrentScene();

		if (scene) {
			for (int i = 0; i <= 3; ++i) {
				color[i] = ((glm::vec4) scene->bgColor)[i];
			}
		}

		glClearColor(color[0], color[1], color[2], color[3]);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	}

	void Renderer::OnRender()
	{
		auto& scene = Engine::GetInstance()->GetCurrentScene();
		// Render 2D
		CameraComponent* mainCamera = nullptr;
		glm::mat4 cameraTransform;
		{
			auto view = scene->Reg().view<TransformComponent, CameraComponent>();
			for (auto entity : view)
			{
				auto [transform, camera] = view.get<TransformComponent, CameraComponent>(entity);

				if (camera.Primary)
				{
					mainCamera = &camera;
					cameraTransform = (glm::mat4)transform;
					break;
				}
			}
		}

		// Reset Stats For RenderAPI
		RenderAPI::ResetStats();

		// Render 2D
		if (mainCamera) {
			auto& xf = mainCamera->entity->xf();
			RenderAPI::Begin(mainCamera->GetProjection() * glm::inverse(cameraTransform));

			auto group = scene->Reg().group<TransformComponent>(entt::get<SpriteComponent>);
			for (auto entity : group)
			{
				auto [transform, sprite] = group.get<TransformComponent, SpriteComponent>(entity);

				if (!sprite.texture) {
					RenderAPI::DrawQuad((glm::mat4)transform,   (glm::vec4) sprite.color);
				}
				else {
					RenderAPI::DrawQuad((glm::mat4)transform, sprite.texture, 1.0f, (glm::vec4) sprite.color);
				}
			}

			RenderAPI::Draw();
		}
	}
}