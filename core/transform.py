from typing import Union, Tuple

from kge.core.component import BaseComponent
from kge.utils.vector import Vector

import math


import Box2D as b2


class Transform(BaseComponent):
    """
    A component that holds position values, angle
    and scale of the entity
    """

    def __init__(self, entity, position: Vector = Vector(0, 0), scale: Vector = Vector.Unit(), angle: float = 0.0):
        super(Transform, self).__init__(entity)

        self._position = Vector.Zero()
        self._angle = 0
        self._scale = Vector.Unit()

        # transform
        self._t = b2.b2Transform()
        self._t.position = position
        self._t.angle = angle

        # set states
        self.angle = angle
        self.position = position
        self.scale = scale

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

        if isinstance(value, tuple):
            vec = Vector(value[0], value[1])
        elif isinstance(value, Vector):
            vec = Vector(value)
        else:
            raise TypeError("Position should be either an tuple of Numbers or a vector")

        offset = vec - self._position
        self._position = vec
        self._t.position = vec

        for child in self.children:  # type: Transform
            child.position += offset

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

            for child in self.children:  # type: Transform
                child.angle = math.radians(rotation)

        else:
            raise TypeError("Angle should be an int or a float")

    def __repr__(self):
        """
        Print this object
        :return:
        """
        return f"Transform : position={self.position}, scale={self.scale}, angle={self.angle} of entity '{self.entity}'"
