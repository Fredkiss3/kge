#pragma once
#include "KGE/Core/Components.h"
#include "LowLevel/Texture.h"
#include "KGE/Utils/Color.h"

namespace KGE {
	struct SpriteComponent : public Component 
	{
		Color color;
		Ref<Texture> texture;

		SpriteComponent() = default;
		/*SpriteComponent(const SpriteComponent& other)
			: texture(other.texture), color(other.color)
		{};*/

		SpriteComponent(const std::string& texPath = "", const Color& color = Color::White())
			: color(color) 
		{
			if(!texPath.empty()) texture = CreateRef<Texture>(texPath);
		}

		SpriteComponent(const Color& col = Color::White(), Ref<Texture> tex = nullptr)
			: color(col), texture(tex) {}

		CC(Sprite);
		CLASS_TYPE(SpriteComponent);
	};


	// For camera Component
	enum class ProjectionType { Perspective = 0, Orthographic = 1 };

	struct CameraComponent : public Component
	{
		bool Primary = false;

		CameraComponent() = default;
		CameraComponent(const glm::mat4& projection)
			: m_Projection(projection) {}

	
		void SetViewportSize(uint32_t width, uint32_t height)
		{
			m_AspectRatio = (float)width / (float)height;
			RecalculateProjection();
		
		}

		ProjectionType GetProjectionType() const { return m_ProjectionType; }
		void SetProjectionType(ProjectionType type) { m_ProjectionType = type; RecalculateProjection(); }


		// Perspective
		void SetPerspective(float verticalFOV, float nearClip, float farClip)
		{
			m_ProjectionType = ProjectionType::Perspective;
			m_PerspectiveFOV = verticalFOV;
			m_PerspectiveNear = nearClip;
			m_PerspectiveFar = farClip;
			RecalculateProjection();
		}

		float GetPerspectiveVerticalFOV() const { return m_PerspectiveFOV; }
		void SetPerspectiveVerticalFOV(float verticalFov) { m_PerspectiveFOV = verticalFov; RecalculateProjection(); }
		float GetPerspectiveNearClip() const { return m_PerspectiveNear; }
		void SetPerspectiveNearClip(float nearClip) { m_PerspectiveNear = nearClip; RecalculateProjection(); }
		float GetPerspectiveFarClip() const { return m_PerspectiveFar; }
		void SetPerspectiveFarClip(float farClip) { m_PerspectiveFar = farClip; RecalculateProjection(); }


		// Ortho
		void SetOrthographic(float size, float nearClip, float farClip)
		{
			m_ProjectionType = ProjectionType::Orthographic;
			m_OrthographicSize = size;
			m_OrthographicNear = nearClip;
			m_OrthographicFar = farClip;
			RecalculateProjection();
		}

		float GetOrthographicSize() const { return m_OrthographicSize; }
		void SetOrthographicSize(float size) { m_OrthographicSize = size; RecalculateProjection(); }
		const glm::mat4& GetProjection() const { return m_Projection; }

		bool FixedAspectRatio = false;
		
	private:
		void RecalculateProjection() 
		{
			if (m_ProjectionType == ProjectionType::Perspective)
			{
				m_Projection = glm::perspective(m_PerspectiveFOV, m_AspectRatio, m_PerspectiveNear, m_PerspectiveFar);
			}
			else
			{
				float orthoLeft = -m_OrthographicSize * m_AspectRatio * 0.5f;
				float orthoRight = m_OrthographicSize * m_AspectRatio * 0.5f;
				float orthoBottom = -m_OrthographicSize * 0.5f;
				float orthoTop = m_OrthographicSize * 0.5f;

				m_Projection = glm::ortho(orthoLeft, orthoRight,
					orthoBottom, orthoTop, m_OrthographicNear, m_OrthographicFar);
			}
		}

	private:
		ProjectionType m_ProjectionType = ProjectionType::Orthographic;

		float m_PerspectiveFOV = glm::radians(45.0f);
		float m_PerspectiveNear = 0.01f, m_PerspectiveFar = 1000.0f;

		float m_OrthographicSize = 10.0f;
		float m_OrthographicNear = -1.0f, m_OrthographicFar = 1.0f;

		float m_AspectRatio = 0.0f;
		glm::mat4 m_Projection = glm::mat4(1.0f);

		CC(Camera);
		CLASS_TYPE(CameraComponent);
	};
}
