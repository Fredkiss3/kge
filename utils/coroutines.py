from collections import Callable

import pyglet

class _Coroutine:
    """
    TODO :
        - TO TEST
        - Reformat with async ?
    """
    def __init__(self, f: Callable, delay=0.01, loop=False):
        self.f = f
        self.loop = loop
        self.delay = delay

    def __call__(self, *args, **kwargs):
        if self.loop:
            pyglet.clock.schedule_interval(lambda dt: self.f(*args, **kwargs), self.delay)
        else:
            pyglet.clock.schedule_once(lambda dt: self.f(*args, **kwargs), self.delay)


# wrap _Coroutine to allow for deferred calling
def coroutine(function=None, delay=0.01, loop=False):
    """
    Coroutines functions

    when setting a function as coroutine, your function should not have an infinite loop in it
    if there is one, it will freeze your game
    instead use loop argument in order to loop your function and use defer the call to your function.

    Coroutines does not return anything.

    Example of use :
        >>> @coroutine
        >>> def greet(name)
        >>>     print("Hello", name)
        >>>
        >>> greet("Fred")

    """
    if function:
        return _Coroutine(function)
    else:
        def wrapper(function):
            return _Coroutine(function, delay, loop)

        return wrapper


if __name__ == '__main__':
    @coroutine(loop=True, delay=1)
    def f(name):
        print(f"Hello {name}")

    f("Fred")
    pyglet.app.run()