workspace "KGE"
	architecture "x86_64"
	startproject "SandBox"

	configurations
	{
		"Debug",
		"Release",
		"Dist"
	}
	
	flags
	{
		"MultiProcessorCompile"
	}

outputdir = "%{cfg.buildcfg}-%{cfg.system}-%{cfg.architecture}"

-- Include directories relative to root folder (solution directory)
IncludeDir = {}
IncludeDir["spdlog"] = "KGE/vendor/spdlog"
IncludeDir["entt"] = "KGE/vendor/entt"
-- IncludeDir["GLFW"] = "Hazel/vendor/GLFW/include"
-- IncludeDir["Glad"] = "Hazel/vendor/Glad/include"
-- IncludeDir["ImGui"] = "Hazel/vendor/imgui"
-- IncludeDir["glm"] = "Hazel/vendor/glm"
-- IncludeDir["stb_image"] = "Hazel/vendor/stb_image"

group "Dependencies"
	-- include "KGE/vendor/spdlog"
	-- include "Hazel/vendor/GLFW"
	-- include "Hazel/vendor/Glad"
	-- include "Hazel/vendor/imgui"
group ""

project "KGE"
	location "KGE"
	kind "StaticLib"
	language "C++"
	cppdialect "C++17"
	staticruntime "on"

	targetdir ("bin/" .. outputdir .. "/%{prj.name}")
	objdir ("bin-int/" .. outputdir .. "/%{prj.name}")

	pchheader "headers.h"
	pchsource "KGE/src/headers.cpp"

	files
	{
		"%{prj.name}/src/**.h",
		"%{prj.name}/src/**.cpp",
		"%{prj.name}/vendor/**.h",
		"%{prj.name}/vendor/**.hpp",
		"%{prj.name}/vendor/**.cpp",
		-- "%{prj.name}/vendor/**.cpp",
	}

	defines
	{
	}

	includedirs
	{
		"%{prj.name}/src",
		"%{prj.name}/vendor/",
	}

	links 
	{ 
	}

	filter "system:windows"
		systemversion "latest"
		defines "K_PLATFORM_WINDOWS"

		defines
		{
		}

	filter "configurations:Debug"
		defines "K_DEBUG"
		runtime "Debug"
		symbols "on"

	filter "configurations:Release"
		defines "K_RELEASE"
		runtime "Release"
		optimize "on"

	filter "configurations:Dist"
		defines "K_DIST"
		runtime "Release"
		optimize "on"

project "Sandbox"
	location "Sandbox"
	kind "ConsoleApp"
	language "C++"
	cppdialect "C++17"
	staticruntime "on"

	targetdir ("bin/" .. outputdir .. "/%{prj.name}")
	objdir ("bin-int/" .. outputdir .. "/%{prj.name}")

	files
	{
		"%{prj.name}/**.h",
		"%{prj.name}/**.cpp"
	}

	includedirs
	{
		"KGE/src",
		"KGE/vendor",
	}

	links
	{
		"KGE"
	}

	filter "system:windows"
		systemversion "latest"
		defines "K_PLATFORM_WINDOWS"
		
	filter "configurations:Debug"
		defines "K_DEBUG"
		runtime "Debug"
		symbols "on"

	filter "configurations:Release"
		defines "K_RELEASE"
		runtime "Release"
		optimize "on"

	filter "configurations:Dist"
		defines "K_DIST"
		runtime "Release"
		optimize "on"

project "EntityComponentSystem"
	location "ECS"
	kind "ConsoleApp"
	language "C++"
	cppdialect "C++17"
	staticruntime "on"

	targetdir ("bin/" .. outputdir .. "/%{prj.name}")
	objdir ("bin-int/" .. outputdir .. "/%{prj.name}")

	files
	{
		"ECS/**.h",
		"ECS/**.cpp"
	}
