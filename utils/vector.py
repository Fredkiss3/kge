from typing import Union, Sequence, Any, List

import math


class Vector:
    """
    A class representing a vector
    """

    def __init__(self, arg1: Union["Vector", float] = 0.0, arg2: float = 0.0):
        if isinstance(arg1, (Vector)):
            self.x = arg1.x
            self.y = arg1.y
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            self.x = arg1
            self.y = arg2
        else:
            raise TypeError(
                "Arguments of vectors should be either another Vector, or x and y values")

    def __eq__(self, other: "Vector"):
        if not isinstance(other, Vector):
            return False
        return self.x == other[0] and self.y == other[1]

    @classmethod
    def Up(cls) -> "Vector":
        """
        :return: A vector pointing up
        """
        return Vector(0, 1)

    @classmethod
    def TopLeft(cls) -> "Vector":
        """
        :return: A vector representing the left up corner
        """
        return Vector(-1 / 2, 1 / 2)

    @classmethod
    def BottomLeft(cls) -> "Vector":
        """
        :return: A vector representing the left bottom corner
        """
        return Vector(-1 / 2, -1 / 2)

    @classmethod
    def TopRight(cls) -> "Vector":
        """
        :return: A vector representing the left up corner
        """
        return Vector(1 / 2, 1 / 2)

    @classmethod
    def BottomRight(cls) -> "Vector":
        """
        :return: A vector representing the left bottom corner
        """
        return Vector(1 / 2, -1 / 2)

    @classmethod
    def Box(self) -> List["Vector"]:
        return [Vector.TopLeft(),
                Vector.TopRight(),
                Vector.BottomRight(),
                Vector.BottomLeft(), ]

    @classmethod
    def Down(cls) -> "Vector":
        """
        :return: A vector pointing down
        """
        return Vector(0, -1)

    @classmethod
    def Left(cls) -> "Vector":
        """
        :return: A vector pointing to the left
        """
        return Vector(-1, 0)

    @classmethod
    def Right(cls) -> "Vector":
        """
        :return: A vector pointing to the right
        """
        return Vector(1, 0)

    @classmethod
    def Zero(cls) -> "Vector":
        """
        Return a zero length vector
        :return:
        """
        return Vector(0, 0)

    @classmethod
    def Unit(self):
        """
        Return a 1 unit vector
        :return:
        """
        return Vector(1, 1)

    def __abs__(self):
        return Vector(abs(self.x), abs(self.y))

    def __iter__(self):
        yield self.x
        yield self.y

    def dot(self, other):
        """The dot product between the vector and other vector
            v1.dot(v2) (v1.v2) -> v1.x*v2.x + v1.y*v2.y

        :return: The dot product
        """
        return float(self.x * other[0] + self.y * other[1])

    def cross(self, other: Union[Sequence[float], "Vector"]):
        """The cross product between the vector and other vector
            v1.cross(v2) (v1xv2) -> v1.x*v2.y - v1.y*v2.x

        :return: The cross product
        """
        return self.x * other[1] - self.y * other[0]

    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def length_sqrd(self):
        return self.x ** 2 + self.y ** 2

    def distance_to(self, other: Union[Sequence[float], "Vector"]) -> float:
        """
        The distance between this vector and another one

        :param other: a vectorLike object which can either be a tuple or a another vector
        :return: float
        """
        return math.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)

    def lerp(self, other: "Vector", p: float):
        """
        Lerp function
        """
        return Vector(self.x + (other[0] - self.x) * p, self.y + (other[1] - self.y) * p)

    @classmethod
    def move_towards(cls, origin: "Vector", dest: "Vector", speed: float):
        """
        Move towards another vector at a given speed
        speed is a normal value
        """
        v = dest - origin
        magnitude = v.length

        if magnitude <= speed or magnitude == 0:
            new_position = dest
        else:
            new_position = Vector(origin + v / magnitude * speed)

        return Vector(new_position)

    def normalized(self):
        length = self.length

        if length != 0:
            return self / length
        return Vector(self)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("Vectors have only two values")

    def normalize(self):
        self.x, self.y = self.normalized().x, self.normalized().y

    def angle_to(self, other: "Vector"):
        """
        Get angle between to vectors in degrees
        """
        cross = self.x * other[1] - self.y * other[0]
        dot = self.x * other[0] + self.y * other[1]
        return math.degrees(math.atan2(cross, dot))

    @property
    def angle(self):
        if (self.length_sqrd == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def __truediv__(self, other: float):
        return Vector(self.x / other, self.y / other)

    def __rtruediv__(self, other: float):
        return Vector(other / self.x, other / self.y)

    def __add__(self, other):
        return Vector(self.x + other[0], self.y + other[1])

    __radd__ = __add__

    def __mul__(self, other: Union[float, "Vector", Sequence[Union[float, int]], Any]):
        if isinstance(other, (float, int)):
            return Vector(self.x * other, self.y * other)
        elif isinstance(other, (Vector, tuple, list)):
            return Vector(self.x * other[0], self.y * other[1])
        else:
            return other * tuple(self)

    __rmul__ = __mul__

    def __sub__(self, other: Union["Vector", Sequence[float]]):
        return Vector(self.x - other[0], self.y - other[1])

    def __rsub__(self, other: Union["Vector", Sequence[float]]):
        return other - self

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __invert__(self):
        return Vector(-self.x, -self.y)

    def rotate(self, angle_d: float):
        """Rotate the vector by 'angle_d' degrees."""
        angle_radians = math.radians(angle_d)
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        self.x = x
        self.y = y

    def rotated(self, angle_d: float):
        """Create and return a new vector by rotating this vector by
        'angle_d' degrees.

        :return: Rotated vector
        """
        angle_radians = math.radians(angle_d)
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vector(x, y)

    def __len__(self):
        return 2


if __name__ == '__main__':
    A = Vector(-2, -2)
    B = Vector(2, 2)
    C = Vector(0, 1)
    D = Vector(1, 0)
    print(abs(A))

    print(A == B)

    print(A / 2)
    print(*A)
    print(A.normalized())
    print(A.length)
    # A.normalize()
    print(A.length)
    print(C.length)
    C.normalize()
    print(C.length)
    print(B.angle_to(C))
    print(A.angle)
    print(C.angle)
    print(D.angle)

    print(A - B)
    print(B - A)

    # print(A.move_towards(B, math.sqrt(2)))

    print(tuple(A))
