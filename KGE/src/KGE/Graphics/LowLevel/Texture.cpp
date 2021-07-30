#include "headers.h"
#include "Texture.h"
#include <stb_image.h>

namespace KGE {

	Texture::Texture(const std::string& path) 
		: m_LocalBuffer(nullptr), m_BPP(0), m_Width(0), m_Height(0), m_FilePath(path)
	{
		// Flip texture vertically
		stbi_set_flip_vertically_on_load(1);
		
		// Load an Image file with transparency
 		m_LocalBuffer = stbi_load(path.c_str(), &m_Width, &m_Height, &m_BPP, 0);
		
		// In case of error
		const std::string output = "The file ";
		K_CORE_ASSERT(m_LocalBuffer,  (output + path.c_str() + " is not a valid Image File").c_str());

		// Generate texture
		glGenTextures(1, &m_RendererID);
		glBindTexture(GL_TEXTURE_2D, m_RendererID);

		// set zoom parameters
		//auto filter = GL_NEAREST;
		//if (!pixelated) filter = GL_LINEAR;
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

		// the texture can be repeated
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

		// Set Blending
		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

		// set texture data
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, m_Width, m_Height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
			m_LocalBuffer);

		// Unbind texture
		glBindTexture(GL_TEXTURE_2D, 0);

		if (m_LocalBuffer)
			stbi_image_free(m_LocalBuffer);
	}

	Texture::Texture(uint32_t width, uint32_t height) 
		: m_Width(width), m_Height(height), m_LocalBuffer(nullptr), m_BPP(0)
	{
		// Generate texture
		glGenTextures(1, &m_RendererID);
		glBindTexture(GL_TEXTURE_2D, m_RendererID);

		// set zoom parameters
		//auto filter = GL_NEAREST;
		//if (!pixelated) filter = GL_LINEAR;
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

		// the texture can be repeated
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

		// Set Blending
		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

		// Set Texture Data
		/*glTexImage2D(GL_TEXTURE_2D, 0,
			GL_RGBA, m_Width, m_Height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
			(void*) 0xffffffff);*/

		//glTexSubImage2D(m_RendererID, 0, 0, 0, m_Width, m_Height, GL_RGBA, GL_UNSIGNED_BYTE, (void *)0xffffffff);
		glBindTexture(GL_TEXTURE_2D, 0);
	}

	Texture::~Texture()
	{
		glDeleteTextures(1, &m_RendererID);
	}

	const void Texture::Bind(int slot) const
	{
		glActiveTexture(GL_TEXTURE0 + slot);
		glBindTexture(GL_TEXTURE_2D, m_RendererID);
	}

	const void Texture::UnBind() const
	{
		glActiveTexture(GL_TEXTURE0);
		glBindTexture(GL_TEXTURE_2D, 0);
	}
}