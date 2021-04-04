#include "headers.h"
#include "VertexArray.h"

namespace KGE {

	static GLenum ShaderToGLType(ShaderType type)
	{
		switch (type)
		{
			case ShaderType::Float:    return GL_FLOAT;
			case ShaderType::Float2:   return GL_FLOAT;
			case ShaderType::Float3:   return GL_FLOAT;
			case ShaderType::Float4:   return GL_FLOAT;
			case ShaderType::Mat3:     return GL_FLOAT;
			case ShaderType::Mat4:     return GL_FLOAT;
			case ShaderType::Int:      return GL_INT;
			case ShaderType::Int2:     return GL_INT;
			case ShaderType::Int3:     return GL_INT;
			case ShaderType::Int4:     return GL_INT;
			case ShaderType::Bool:     return GL_BOOL;
		}

		K_CORE_ASSERT(false, "Unknown ShaderDataType!");
		return 0;
	}

	VertexArray::VertexArray()
	{
		glGenVertexArrays(1, &m_RendererID);
		glBindVertexArray(m_RendererID);
	}

	VertexArray::~VertexArray()
	{
		glDeleteVertexArrays(1, &m_RendererID);
	}

	const void VertexArray::Bind() const
	{
		glBindVertexArray(m_RendererID);
	}

	const void VertexArray::UnBind() const
	{
		glBindVertexArray(0);
	}

	void VertexArray::AddVertexBuffer(const Ref<VertexBuffer>& vertexBuffer)
	{
		

		K_CORE_ASSERT(vertexBuffer->GetLayout().GetElements().size(), "Vertex Buffer has no layout!");

		glBindVertexArray(m_RendererID);
		vertexBuffer->Bind();

		const auto& layout = vertexBuffer->GetLayout();
		for (const auto& element : layout)
		{
			switch (element.Type)
			{
				case ShaderType::Float:
				case ShaderType::Float2:
				case ShaderType::Float3:
				case ShaderType::Float4:
				case ShaderType::Int:
				case ShaderType::Int2:
				case ShaderType::Int3:
				case ShaderType::Int4:
				case ShaderType::Bool:
			{
				glEnableVertexAttribArray(m_VertexBufferIndex);
				glVertexAttribPointer(m_VertexBufferIndex,
					element.GetComponentCount(),
					ShaderToGLType(element.Type),
					element.Normalized ? GL_TRUE : GL_FALSE,
					layout.GetStride(),
					(const void*)element.Offset);
				m_VertexBufferIndex++;
				break;
			}
			case ShaderType::Mat3:
			case ShaderType::Mat4:
			{
				uint8_t count = element.GetComponentCount();
				for (uint8_t i = 0; i < count; i++)
				{
					glEnableVertexAttribArray(m_VertexBufferIndex);
					glVertexAttribPointer(m_VertexBufferIndex,
						count,
						ShaderToGLType(element.Type),
						element.Normalized ? GL_TRUE : GL_FALSE,
						layout.GetStride(),
						(const void*)(sizeof(float) * count * i));
					glVertexAttribDivisor(m_VertexBufferIndex, 1);
					m_VertexBufferIndex++;
				}
				break;
			}
			default:
				K_CORE_ASSERT(false, "Unknown ShaderDataType!");
			}
		}

		m_VertexBuffers.push_back(vertexBuffer);
	}

	void VertexArray::SetIndexBuffer(const Ref<IndexBuffer>& indexBuffer)
	{
		glBindVertexArray(m_RendererID);
		indexBuffer->Bind();

		m_IndexBuffer = indexBuffer;
	}


}