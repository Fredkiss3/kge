#pragma once

#include "headers.h"
#include "KGE/Base.h"
#include "spdlog/spdlog.h"
#include "spdlog/fmt/ostr.h" 
#include "spdlog/sinks/stdout_color_sinks.h"

namespace KGE
{
	enum class LogLevel
	{
		TRACE,
		INFO,
		WARN,
		ERR,
		CRITICAL,
		DEBUG,
	};

	class Logger
	{
	public:
		static void Init();
		static void SetLogLevel(LogLevel level);

		static std::shared_ptr<spdlog::logger>& GetClientLogger() { return s_ClientLogger; }
		static std::shared_ptr<spdlog::logger>& GetCoreLogger() { return s_CoreLogger; }

	private:
		static std::shared_ptr<spdlog::logger> s_CoreLogger;
		static std::shared_ptr<spdlog::logger> s_ClientLogger;
	};

} // namespace KGE

// Core log macros
#ifdef K_DEBUG
#define K_CORE_TRACE(...) ::KGE::Logger::GetCoreLogger()->trace(__VA_ARGS__)
#define K_CORE_INFO(...) ::KGE::Logger::GetCoreLogger()->info(__VA_ARGS__)
#define K_CORE_WARN(...) ::KGE::Logger::GetCoreLogger()->warn(__VA_ARGS__)
#define K_CORE_ERROR(...) ::KGE::Logger::GetCoreLogger()->error(__VA_ARGS__)
#define K_CORE_DEBUG(...) ::KGE::Logger::GetCoreLogger()->debug(__VA_ARGS__)
#define K_CORE_CRITICAL(...) ::KGE::Logger::GetCoreLogger()->critical(__VA_ARGS__)

// Client log macros
#define K_TRACE(...) ::KGE::Logger::GetClientLogger()->trace(__VA_ARGS__)
#define K_INFO(...) ::KGE::Logger::GetClientLogger()->info(__VA_ARGS__)
#define K_WARN(...) ::KGE::Logger::GetClientLogger()->warn(__VA_ARGS__)
#define K_ERROR(...) ::KGE::Logger::GetClientLogger()->error(__VA_ARGS__)
#define K_CRITICAL(...) ::KGE::Logger::GetClientLogger()->critical(__VA_ARGS__)
#else
#define K_CORE_TRACE(...)
#define K_CORE_INFO(...) 
#define K_CORE_WARN(...) 
#define K_CORE_ERROR(...)
#define K_CORE_DEBUG(...)
#define K_CORE_CRITICAL(...)


#define K_TRACE(...)
#define K_INFO(...) 
#define K_WARN(...) 
#define K_ERROR(...)
#define K_CRITICAL(...)
#endif