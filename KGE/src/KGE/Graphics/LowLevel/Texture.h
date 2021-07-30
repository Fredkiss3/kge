#pragma once
#include "headers.h"
#include "KGE/Base.h"
#include "GLObject.h"

namespace KGE {
	class Texture : public GLObject
	{
	public:
		~Texture();
		Texture(const std::string& path);
		Texture(uint32_t width, uint32_t height);

		const void Bind(int slot) const;
		const void UnBind() const override;

		const void Bind() const override { Bind(0); };

		uint32_t GetWidth() { return m_Width; };
		uint32_t GetHeight() { return m_Height; };

		bool operator==(const Texture& other) const
		{
			return m_RendererID == other.m_RendererID;
		}
	private:
		int m_Width, m_Height, m_BPP;
		GLuint m_RendererID;
		std::string m_FilePath;
		unsigned char* m_LocalBuffer;
	};

}
