class InputMeta(type):
    """
    Metaclass for Input. You probably want that instead.
    """

    def __new__(mcls, *p, abstract=False, **kw):
        cls = super().__new__(mcls, *p, **kw)
        if abstract:
            cls._instance = ...
            return cls
        else:
            cls._instance = None
            return cls()

    def __call__(cls):
        if cls._instance is None:
            cls._instance = type.__call__(cls)
        elif cls._instance is ...:
            raise TypeError("Cannot instantiate abstract input")
        return cls._instance


class Input(metaclass=InputMeta, abstract=True):
    """
    Inherit from Input to make a simple input.

    Add abstract=True in the class line to make an input type.
    """

