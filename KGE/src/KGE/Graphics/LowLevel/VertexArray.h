#pragma once
#include "KGE/Base.h"
#include "Buffer.h"

namespace KGE {
	class VertexArray: public GLObject 
	{
	public:
		VertexArray();
		 ~VertexArray();

		 const void Bind() const override;
		 const void UnBind() const override;

		 void AddVertexBuffer(const Ref<VertexBuffer>& vertexBuffer) ;
		 void SetIndexBuffer(const Ref<IndexBuffer>& indexBuffer) ;

		 const std::vector<Ref<VertexBuffer>>& GetVertexBuffers() const { return m_VertexBuffers; }
		 const Ref<IndexBuffer>& GetIndexBuffer() const { return m_IndexBuffer; }
	private:
		uint32_t m_RendererID;
		uint32_t m_VertexBufferIndex = 0;
		std::vector<Ref<VertexBuffer>> m_VertexBuffers;
		Ref<IndexBuffer> m_IndexBuffer;
	};

}