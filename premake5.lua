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
IncludeDir["spdlog"] = "KGE/vendor/spdlog/include"
IncludeDir["entt"] = "KGE/vendor/entt/include"
IncludeDir["GLFW"] = "KGE/vendor/GLFW/include"
IncludeDir["Glad"] = "KGE/vendor/Glad/include"
IncludeDir["box2d"] = "KGE/vendor/box2d/include"
IncludeDir["ImGui"] = "KGE/vendor/imgui"
IncludeDir["glm"] = "KGE/vendor/glm"
IncludeDir["stb_image"] = "KGE/vendor/stb_image"

group "Dependencies"
	include "KGE/vendor/GLFW"
	include "KGE/vendor/Glad"
	include "KGE/vendor/imgui"
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
		"%{prj.name}/vendor/stb_image/**.h",
		"%{prj.name}/vendor/stb_image/**.cpp",
		"%{prj.name}/vendor/glm/glm/**.hpp",
		"%{prj.name}/vendor/glm/glm/**.inl",
		"%{prj.name}/vendor/box2d/src/**.cpp",
		"%{prj.name}/vendor/box2d/src/**.h",
	}

	defines
	{
		"_CRT_SECURE_NO_WARNINGS",
		"GLFW_INCLUDE_NONE"
	}

	includedirs
	{
		"%{prj.name}/src",
		"%{IncludeDir.entt}",
		"%{IncludeDir.spdlog}",
		"%{IncludeDir.Glad}",
		"%{IncludeDir.GLFW}",
		"%{IncludeDir.ImGui}",
		"%{IncludeDir.glm}",
		"%{IncludeDir.box2d}",
		"%{IncludeDir.stb_image}",
	}

	links 
	{ 
		"GLFW",
		"Glad",
		"ImGui",
		"opengl32.lib"
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
		"%{IncludeDir.entt}",
		"%{IncludeDir.spdlog}",
		"%{IncludeDir.Glad}",
		"%{IncludeDir.GLFW}",
		"%{IncludeDir.ImGui}",
		"%{IncludeDir.glm}",
		"%{IncludeDir.box2d}",
		"%{IncludeDir.stb_image}",
	}

	links
	{
		"KGE"
	}

	defines
	{
		"_CRT_SECURE_NO_WARNINGS",
		"GLFW_INCLUDE_NONE"
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
