from kge.inputs.input import Input


class MouseInput(Input, abstract=True):
    """
    A mouse input
    """


class Left(MouseInput):
    """
    Primary mouse button (commonly left)
    """


class Right(MouseInput):
    """
    Secondary mouse button (commonly right)
    """


class Middle(MouseInput):
    """
    Third mouse button (commonly middle)
    """


class WheelDown(MouseInput):
    """
    Mouse wheel scrolled down ?
    """


class WheelUp(MouseInput):
    """
    Mouse wheel scrolled up ?
    """