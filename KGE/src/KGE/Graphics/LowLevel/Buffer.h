#pragma once
#include "GLObject.h"
#include "KGE/Base.h"

namespace  KGE {

	enum class ShaderType
	{
		None = 0, Float, Float2, Float3, Float4, Mat3, Mat4, Int, Int2, Int3, Int4, Bool
	};

	static uint32_t ShaderTypeSize(ShaderType type)
	{
		switch (type)
		{
		case ShaderType::Float:    return 4;
		case ShaderType::Float2:   return 4 * 2;
		case ShaderType::Float3:   return 4 * 3;
		case ShaderType::Float4:   return 4 * 4;
		case ShaderType::Mat3:     return 4 * 3 * 3;
		case ShaderType::Mat4:     return 4 * 4 * 4;
		case ShaderType::Int:      return 4;
		case ShaderType::Int2:     return 4 * 2;
		case ShaderType::Int3:     return 4 * 3;
		case ShaderType::Int4:     return 4 * 4;
		case ShaderType::Bool:     return 1;
		}

		K_CORE_ASSERT(false, "Unknown Shader Type!");
		return 0;
	}

	struct BufferElement
	{
		std::string Name;
		ShaderType Type;
		uint32_t Size;
		size_t Offset;
		bool Normalized;

		BufferElement() = default;

		BufferElement(ShaderType type, const std::string& name, bool normalized = false)
			: Name(name), Type(type), Size(ShaderTypeSize(type)), Offset(0), Normalized(normalized)
		{
		}

		uint32_t GetComponentCount() const
		{
			switch (Type)
			{
			case ShaderType::Float:   return 1;
			case ShaderType::Float2:  return 2;
			case ShaderType::Float3:  return 3;
			case ShaderType::Float4:  return 4;
			case ShaderType::Mat3:    return 3; // 3* float3
			case ShaderType::Mat4:    return 4; // 4* float4
			case ShaderType::Int:     return 1;
			case ShaderType::Int2:    return 2;
			case ShaderType::Int3:    return 3;
			case ShaderType::Int4:    return 4;
			case ShaderType::Bool:    return 1;
			}

			K_CORE_ASSERT(false, "Unknown ShaderDataType!");
			return 0;
		}
	};

	class BufferLayout
	{
	public:
		BufferLayout() {}

		BufferLayout(const std::initializer_list<BufferElement>& elements)
			: m_Elements(elements)
		{
			CalculateOffsetsAndStride();
		}

		uint32_t GetStride() const { return m_Stride; }
		const std::vector<BufferElement>& GetElements() const { return m_Elements; }

		std::vector<BufferElement>::iterator begin() { return m_Elements.begin(); }
		std::vector<BufferElement>::iterator end() { return m_Elements.end(); }
		std::vector<BufferElement>::const_iterator begin() const { return m_Elements.begin(); }
		std::vector<BufferElement>::const_iterator end() const { return m_Elements.end(); }
	private:
		void CalculateOffsetsAndStride()
		{
			size_t offset = 0;
			m_Stride = 0;
			for (auto& element : m_Elements)
			{
				element.Offset = offset;
				offset += element.Size;
				m_Stride += element.Size;
			}
		}
	private:
		std::vector<BufferElement> m_Elements;
		uint32_t m_Stride = 0;
	};



	class VertexBuffer : public GLObject {
	private:
		BufferLayout m_Layout;
	public:
		VertexBuffer(uint32_t size);
		VertexBuffer(const void* data, uint32_t size);
		~VertexBuffer();

		void SetData(const void* data, uint32_t size);
		const void Bind() const override;
		const void UnBind() const override;

		virtual const BufferLayout& GetLayout() const { return m_Layout; }
		virtual void SetLayout(const BufferLayout& layout) { m_Layout = layout; }
	};

	class IndexBuffer : public GLObject {
	private:
		uint32_t m_Count;
	public:
		IndexBuffer(uint32_t* indices, uint32_t count);
		~IndexBuffer();
		const void Bind() const override;
		const void UnBind() const override;

		uint32_t GetCount() const { return m_Count; }
	};
}
