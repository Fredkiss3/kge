#pragma once

#include <memory>
#include <iostream>
#include <KGE/Core/Log.h>

#define K_PLATFORM_WINDOWS
#define K_DEBUG

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
        K_ERROR("Assertion Failed: {0}", __VA_ARGS__); \
        K_DEBUGBREAK();                                \
    }
#define K_CORE_ASSERT(x, ...)                               \
    if (!(x))                                               \
    {                                                       \
        K_CORE_ERROR("Assertion Failed: {0}", __VA_ARGS__); \
        K_DEBUGBREAK();                                     \
    }
#endif
#else
#define K_ASSERT(x, ...)
#define K_CORE_ASSERT(x, ...)
#endif // K_ENABLE_ASSERTS

// To Convert a function that takes an event to an object
#define K_BIND_EVENT_FN(fn) std::bind(&fn, this, std::placeholders::_1)

// include these to work
#include <string>
#include <typeinfo>

std::string demangle(const char *name);

template <class T>
std::string type(const T &t)
{
    return demangle(typeid(t).name());
}
