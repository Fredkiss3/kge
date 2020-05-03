from dataclasses import dataclass
from pyglet.gl import *

from kge.utils.vector import Vector


@dataclass
class Shape:
    """Shapes are drawing primitives that are good for rapid prototyping."""

    # def __init__(self):
    num_points: int
    vertices = [Vector.Zero()]
    mode: int


@dataclass
class Square(Shape):
    """
    A square image of a single color.
    """

    # def __init__(self):
    #     super().__init__()
    vertices = [
        Vector(-1 / 2, 1 / 2),
        Vector(1 / 2, 1 / 2),
        Vector(1 / 2, -1 / 2),
        Vector(-1 / 2, -1 / 2),
    ]
    mode: int = GL_QUADS
    num_points: int = 4


@dataclass
class OutLinedSquare(Square):
    """
    An outlined square of a single color.
    """

    vertices = [
        # Horizontal
        Vector(-1 / 2, 1 / 2),
        Vector(1 / 2, 1 / 2),
        Vector(1 / 2, -1 / 2),
        Vector(-1 / 2, -1 / 2),
        # Vertical
        Vector(-1 / 2, -1 / 2),
        Vector(-1 / 2, 1 / 2),
        Vector(1 / 2, 1 / 2),
        Vector(1 / 2, -1 / 2),
    ]
    mode: int = GL_LINES
    num_points: int = 8


@dataclass
class Triangle(Shape):
    """
    A triangle image of a single color.
    """

    vertices = [
        Vector(0, 1 / 2),
        Vector(1 / 2, -1 / 2),
        Vector(-1 / 2, -1 / 2),
    ]
    num_points: int = 3
    mode: int = GL_TRIANGLES


@dataclass
class OutlinedTriangle(Triangle):
    vertices = [
        # First Line
        Vector(0, 1 / 2),
        Vector(1 / 2, -1 / 2),

        # Second Line
        Vector(1 / 2, -1 / 2),
        Vector(-1 / 2, -1 / 2),

        # Third Line
        Vector(-1 / 2, -1 / 2),
        Vector(0, 1 / 2),
    ]
    num_points: int = 6
    mode: int = GL_LINES


@dataclass
class Circle(Shape):
    """
    A circle image of a single color.
    """
    radius: float = None
    center: Vector = Vector(0, 0)
    num_points: int = 20
    mode: int = GL_TRIANGLE_FAN


@dataclass
class OutlinedCircle(Circle):
    radius: float = None
    center: Vector = Vector(0, 0)
    mode: int = GL_LINE_LOOP
    num_points: int = 20
