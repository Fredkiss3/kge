#include <headers.h>
#include "Log.h"

namespace KGE
{
    std::shared_ptr<spdlog::logger> Logger::s_CoreLogger = nullptr;
    std::shared_ptr<spdlog::logger> Logger::s_ClientLogger = nullptr;

    void Logger::Init()
    {
        // Set Log Pattern
        spdlog::set_pattern("%^[%c] [%l] [%n] : %v%$");

        // Set Loggers
        s_CoreLogger = spdlog::stdout_color_mt("KGE");
        s_ClientLogger = spdlog::stdout_color_mt("Game");

        // Set levels
        s_CoreLogger->set_level(spdlog::level::err);
        s_ClientLogger->set_level(spdlog::level::err);
    }

    void Logger::SetLogLevel(LogLevel level)
    {
        // Should call Init Before
        K_CORE_ASSERT((s_CoreLogger != nullptr), "Core Logger Not Initiliazed");
        K_CORE_ASSERT((s_ClientLogger != nullptr), "Client Logger Not Initiliazed");

        switch (level)
        {
        case LogLevel::ERR:
            s_CoreLogger->set_level(spdlog::level::err);
            s_ClientLogger->set_level(spdlog::level::err);
            break;
        case LogLevel::WARN:
            s_CoreLogger->set_level(spdlog::level::warn);
            s_ClientLogger->set_level(spdlog::level::warn);
            break;
        case LogLevel::INFO:
            s_CoreLogger->set_level(spdlog::level::info);
            s_ClientLogger->set_level(spdlog::level::info);
            break;
        case LogLevel::CRITICAL:
            s_CoreLogger->set_level(spdlog::level::critical);
            s_ClientLogger->set_level(spdlog::level::critical);
            break;
        case LogLevel::DEBUG:
            s_CoreLogger->set_level(spdlog::level::debug);
            s_ClientLogger->set_level(spdlog::level::debug);
            break;
        default:
            s_CoreLogger->set_level(spdlog::level::trace);
            s_ClientLogger->set_level(spdlog::level::trace);
            break;
        }
    }
} // namespace KGE