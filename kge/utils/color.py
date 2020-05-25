class Color:
    """
    An object that represent a color
    """

    def __init__(self, r: int = 255, g: int = 255, b: int = 255, a: float = 1.0):
        self._r = 255
        self._g = 255
        self._b = 255
        self._a = 1.0

        # Set properties
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def __iter__(self):
        return (c for c in [self.red, self.green, self.blue, int(self.alpha * 255)])

    @property
    def red(self):
        return self._r

    @red.setter
    def red(self, val: int):
        if not isinstance(val, int):
            raise TypeError("Red property should be an integer between 0 & 255")

        if not (0 <= val <= 255):
            raise TypeError("Red property should be an integer between 0 & 255")

        self._r = val

    @property
    def blue(self):
        return self._b

    @blue.setter
    def blue(self, val: int):
        if not isinstance(val, int):
            raise TypeError("Blue property should be an integer between 0 & 255")

        if not (0 <= val <= 255):
            raise TypeError("Blue property should be an integer between 0 & 255")

        self._b = val

    @property
    def green(self):
        return self._g

    @green.setter
    def green(self, val: int):
        if not isinstance(val, int):
            raise TypeError("Green property should be an integer between 0 & 255")

        if not (0 <= val <= 255):
            raise TypeError("Green property should be an integer between 0 & 255")

        self._g = val

    @property
    def alpha(self):
        return self._a

    @alpha.setter
    def alpha(self, val: float):
        if not isinstance(val, (int, float)):
            raise TypeError("Alpha property should be a float between 0 & 1")

        if not (0 <= val <= 1):
            raise TypeError("Alpha property should be a float between 0 & 1")

        self._a = float(val)

    def __getitem__(self, item):
        return tuple(self)[item]

    def __mul__(self, n: float):
        if not isinstance(n, (float, int)):
            raise TypeError(f"Can only multiply a Color object with a number")

        if n < 0:
            raise ValueError("Cannot multiply a color with a negative number")

        a = (self.alpha * n)
        if a > 1:
            a = 1

        r = int(self.red * n)
        if r > 255:
            r = 255

        g = int(self.green * n)
        if g > 255:
            g = 255

        b = int(self.blue * n)
        if b > 255:
            b = 255

        return Color(r, g, b, a)

    def __sub__(self, other: "Color"):
        if not isinstance(other, Color):
            raise TypeError(f"Cannot add a Color object with a {type(other).__name__} object")
        else:
            a = abs(self.alpha + other.alpha)
            if a > 1:
                a = 1

            r = abs(self.red - other.red)
            if r > 255:
                r = 255

            g = abs(self.green - other.green)
            if g > 255:
                g = 255

            b = abs(self.blue - other.blue)
            if b > 255:
                b = 255

            return Color(r, g, b, a)

    def __add__(self, other: "Color"):
        if not isinstance(other, Color):
            raise TypeError(f"Cannot add a Color object with a {type(other).__name__} object")
        else:
            a = (self.alpha + other.alpha)
            if a > 1:
                a = 1

            r = (self.red + other.red)
            if r > 255:
                r = 255

            g = (self.green + other.green)
            if g > 255:
                g = 255

            b = (self.blue + other.blue)
            if b > 255:
                b = 255

            return Color(r, g, b, a)

    def __repr__(self):
        return f"Color(red={self._r}, green={self._g}, blue={self._b}, alpha={self._a})"

    def __eq__(self, other: "Color"):
        if isinstance(other, Color):
            return (
                    other._a == self._a
                    and other._r == self._r
                    and other._g == self._g
                    and other._b == self._b
            )
        else:
            return False


if __name__ == '__main__':
    print(Color())
    print(Color() == Color())

    red = Color(g=0, b=0)
    green = Color(r=0, b=0)
    blue = Color(r=0, g=0)
    yellow = red + green

    c = red + (blue - red) * .9
    c2 = blue + (red - blue) * .9
    print(c, c2, c == c2)
