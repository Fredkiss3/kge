#include "headers.h"
#include "Buffer.h"

namespace KGE {

	/**
	**************************************
	*
	*		    VERTEX BUFFER
	*
	*************************************
	*/

	VertexBuffer::VertexBuffer(uint32_t size) {
		// generate a vertex buffer & pass data into it
		glGenBuffers(1, &m_RendererID);
		glBindBuffer(GL_ARRAY_BUFFER, m_RendererID);
		glBufferData(GL_ARRAY_BUFFER, size, nullptr, GL_DYNAMIC_DRAW);
	}


	VertexBuffer::VertexBuffer(const void* data, uint32_t size)
	{
		glGenBuffers(1, &m_RendererID);
		glBindBuffer(GL_ARRAY_BUFFER, m_RendererID);
		glBufferData(GL_ARRAY_BUFFER, size, data, GL_DYNAMIC_DRAW);
	}

	VertexBuffer::~VertexBuffer() {
		glDeleteBuffers(1, &m_RendererID);
	}

	void VertexBuffer::SetData(const void* data, uint32_t size)
	{
		glBindBuffer(GL_ARRAY_BUFFER, m_RendererID);
		glBufferSubData(GL_ARRAY_BUFFER, 0, size, data);
	}

	const void VertexBuffer::Bind() const {
		glBindBuffer(GL_ARRAY_BUFFER, m_RendererID);
	}

	const void VertexBuffer::UnBind() const {
		glBindBuffer(GL_ARRAY_BUFFER, 0);
	}

	/**
	**************************************
	* 
	*			INDEX BUFFER
	*
	*************************************
	*/

	IndexBuffer::IndexBuffer(uint32_t* indices, uint32_t count): m_Count(count) {
		// generate a vertex buffer & pass data into it
		glGenBuffers(1, &m_RendererID);
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, m_RendererID);
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, count * sizeof(uint32_t), indices, GL_STATIC_DRAW);
	}

	IndexBuffer::~IndexBuffer() {
		glDeleteBuffers(1, &m_RendererID);
	}


	const void IndexBuffer::Bind() const
	{
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, m_RendererID);
	}

	const void IndexBuffer::UnBind() const
	{
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
	}
}