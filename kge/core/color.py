class Color:
    """
    An object that represent a color
    """

    def __init__(self, r: int = 255, g: int = 255, b: int = 255, a: float = 1.0):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def __iter__(self):
        return (c for c in [self.red, self.green, self.blue, self.alpha * 255])
