from collections import Callable

import pyglet


class _Coroutine:
    """
    Implementation of coroutines
    """

    def __init__(self, f: Callable, delay: float = 0.01, loop: bool = False):
        self._f = f
        self.loop = loop
        self.delay = delay
        self._call_function = None

    def __call__(self, *args, **kwargs):
        self._call_function = lambda dt: self._f(*args, **kwargs)
        if self.loop:
            pyglet.clock.schedule_interval(self._call_function, self.delay)
        else:
            pyglet.clock.schedule_once(self._call_function, self.delay)

    def stop_loop(self):
        """
        Stop the coroutine
        """
        pyglet.clock.unschedule(self._call_function)


# wrap _Coroutine to allow for deferred calling
def coroutine(function: Callable = None, delay: float = 0.01, loop: bool = False):
    """
    Coroutines functions, functions meant to be ran asynchronously.

    when setting a function as coroutine, your function should not have an infinite loop in it
    if there is one, it will freeze your game
    instead use loop argument in order to loop your function and use delay argument to defer the call to your function,
    or in order to

    Coroutines does not return anything.

    Example of use :
        >>> @coroutine
        >>> def greet(name)
        >>>     print("Hello", name)
        >>>
        >>> greet("Fred")

    Right now you cannot use  « @coroutine » decorator in a method, in order to do so, you should pass
    the method with the object that calls it on the coroutine function.
    Here is how !
        >>> class Player:
        >>>     def yodele(self, name)
        >>>         print("YODELE", name, "!")
        >>>
        >>>     def call_yodele(self, name):
        >>>         c = coroutine(self.yodele)
        >>>         c(name)
        >>>
        >>> p = Player()
        >>> p.call_yodele("hi hou !")
        >>> Output : "YODELE hi hou !"

    """
    if function is not None and not callable(function):
        raise TypeError("Coroutines accept only functions as parameters.")
    else:
        if not (isinstance(delay, (int, float)) and isinstance(loop, bool)):
            raise TypeError(
                "Couroutine Delay argument should be a number and loop argument should be a bool")

    if function:
        return _Coroutine(function, delay, loop)
    else:
        def wrapper(function):
            return _Coroutine(function, delay, loop)

        return wrapper

Coroutine = _Coroutine

if __name__ == '__main__':
    @coroutine(loop=True, delay=.1)
    def f():
        pyglet.media.load()

    f()
    pyglet.app.run()

    #

    class O:
        def m(self):
            pass

    o = O()
    f = o.m
    print(f.__self__, "\n", f, "\n", o.m)

    pass
