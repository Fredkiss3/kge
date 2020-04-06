import math
from typing import Union, Tuple, List

# import Box2D as b2
import sys

import platform
if sys.platform == "win32":
    if platform.architecture()[0] == "64bit":
        import kge.extra.win64.Box2D as b2
    elif platform.architecture()[0] == "32bit":
        import kge.extra.win32.Box2D as b2
else:
    # TODO: make for linux
    pass

from kge.core.component import BaseComponent
from kge.utils.vector import Vector


class Transform(BaseComponent):
    """
    A component that holds position values, angle
    and scale of the entity
    """

    def __init__(self, entity, position: Vector = Vector(0, 0), scale: Vector = Vector.Unit(), angle: float = 0.0):
        super(Transform, self).__init__(entity)

        # The primary attributes of the transform
        self._position = Vector.Zero()
        self._angle = 0
        self._scale = Vector.Unit()

        # Parent-Child Relationship
        self._children = []  # type: List[Transform]
        self._parent = None  # type: Union[Transform, None]

        # transform
        self._t = b2.b2Transform()
        self._t.position = position
        self._t.angle = angle

        # set states
        self.angle = angle
        self.position = position
        self.scale = scale

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value: "Transform"):
        if isinstance(value, Transform):
            self._parent = value
            value.children.append(self)

        elif value is None:
            # remove self from children
            self._parent.children.remove(self)

            # set parent to None
            self._parent = None
        else:
            raise TypeError("parent Should be of type 'kge.core.Transform'")

    @property
    def scale(self) -> Vector:
        return self._scale

    @scale.setter
    def scale(self, value):
        if isinstance(value, (Vector)):
            self._scale = value
        else:
            raise TypeError("Scale should be a vector (scaleX, scaleY)")

    @property
    def position(self):
        return Vector(self._position.x, self._position.y)

    @position.setter
    def position(self, value: Union[
        Tuple[float, float], Vector]):

        if isinstance(value, (tuple, Vector)):
            vec = Vector(value)
        else:
            raise TypeError(
                "Position should be either a tuple of Numbers or a vector")

        offset = vec - self._position
        self._position = vec
        self._t.position = vec

        # TODO : TO TEST
        for child in self.children:  # type: Transform
            child.entity.position += offset

    @property
    def angle(self):
        """
        Return angle in degrees
        """
        return math.degrees(self._angle)

    def __mul__(self, other: Vector):
        return Vector((self._t * tuple(other)).x, (self._t * tuple(other)).y)

    @angle.setter
    def angle(self, value: float):
        """
        Set angle in degrees
        """
        if isinstance(value, (int, float)):
            rotation = value - self.angle

            self._angle = math.radians(value)
            self._t.angle = math.radians(value)

            # TODO : TO TEST
            for child in self.children:  # type: Transform
                child.entity.angle += rotation

        else:
            raise TypeError("Angle should be an int or a float")

    def __repr__(self):
        """
        Print this object
        :return:
        """
        return f"Transform : position={self.position}, scale={self.scale}, angle={self.angle} of entity '{self.entity}'"
