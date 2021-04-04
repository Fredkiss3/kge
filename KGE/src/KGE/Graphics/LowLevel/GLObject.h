#pragma once
#include <glad/glad.h>

class GLObject
{
public:
	GLObject(): m_RendererID(0) {}

	virtual const void Bind() const {};
	virtual const void UnBind() const = 0;
protected:
	GLuint m_RendererID;
};
