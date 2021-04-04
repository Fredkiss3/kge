#pragma once

#include <headers.h>
#include <memory>
#include <iostream>
#include <KGE/Utils/Log.h>

#define CLASS_TYPE(type)                                        \
    static const char *GetStaticType() { return #type; } \
    virtual const char *GetType() const override { return GetStaticType(); }
#define EVENT_TYPE(type) #type


//#define K_PLATFORM_WINDOWS
//#define K_DEBUG

#define TYPE_NAME \
    virtual std::string GetTypeName() { return type(*this); }

#ifdef K_DEBUG
#ifdef K_PLATFORM_WINDOWS
#define K_DEBUGBREAK() __debugbreak();
#elif defined(K_PLATFORM_LINUX)
#include <signal.h>
#define K_DEBUGBREAK() raise(SIGTRAP)
#else
#error KGE Only Support Windows & Linux !
#endif // K_PLATFORM_WINDOWS

#define K_ENABLE_ASSERTS
#else
#define K_DEBUGBREAK()
#endif // K_DEBUG

#ifdef K_ENABLE_ASSERTS
// TO GET Python Asserts Exceptions
#ifdef USE_EXCEPTIONS
#include <Python.h>
class AssertException
{
};
#define K_ASSERT(A, ...)                           \
    if (!(A))                                      \
    {                                              \
        PyErr_SetString(PyExc_AssertionError, #A); \
        throw AssertException();                   \
    }
#define K_CORE_ASSERT(A, ...)                      \
    if (!(A))                                      \
    {                                              \
        PyErr_SetString(PyExc_AssertionError, #A); \
        throw AssertException();                   \
    }
#else
#define K_ASSERT(x, ...)                               \
    if (!x)                                            \
    {                                                  \
        K_ERROR("Assertion Failed [{0}:{1}]: {2} ", __FILE__, __LINE__,__VA_ARGS__); \
        K_DEBUGBREAK();                                \
    }
#define K_CORE_ASSERT(x, ...)                               \
    if (!(x))                                               \
    {                                                       \
        K_CORE_ERROR("Assertion Failed [{0}:{1}]: {2} ", __FILE__, __LINE__,__VA_ARGS__); \
        K_DEBUGBREAK();                                     \
    }
#endif
#else
#define K_ASSERT(x, ...)
#define K_CORE_ASSERT(x, ...)
#endif // K_ENABLE_ASSERTS

// To Convert a member function to a function pointer
#define K_BIND_EVENT_FN(fn) [this](auto&&... args) -> decltype(auto) { return this->fn(std::forward<decltype(args)>(args)...); } 
//std::bind(&fn, this, std::placeholders::_1)

// include these to work
#include <string>
#include <typeinfo>

std::string demangle(const char* name);

template <class T>
std::string type(const T& t)
{
	return demangle(typeid(t).name());
}

template <class T>
std::string type()
{
	return demangle(typeid(T).name());
}

namespace KGE
{
	template <typename T>
	using Scope = std::unique_ptr<T>;
	template <typename T, typename... Args>
	constexpr Scope<T> CreateScope(Args&&... args)
	{
		return std::make_unique<T>(std::forward<Args>(args)...);
	}

	template <typename T>
	using Ref = std::shared_ptr<T>;
	template <typename T, typename... Args>
	constexpr Ref<T> CreateRef(Args&&... args)
	{
		return std::make_shared<T>(std::forward<Args>(args)...);
	}

	template <typename T, typename Y>
	T* castRef(Ref<Y> ref)
	{
		return dynamic_cast<T*>(&(*ref));
	}
} // namespace KGE
