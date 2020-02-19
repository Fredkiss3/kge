import random
from typing import Union, Sequence, Tuple

import math
import pyglet
from pyglet.gl import *

import kge
from kge.resources import events
from kge.utils.vector import Vector
from kge.core.component import BaseComponent
from kge.graphics.image import Image

from kge.core.constants import (
    DEFAULT_SPRITE_RESOLUTION,
    DEFAULT_SPRITE_SIZE,
    DEFAULT_PIXEL_RATIO
)


class Shape:
    """Shapes are drawing primitives that are good for rapid prototyping."""

    def __init__(self, color: Sequence[int]):
        self.color = (color[0], color[1], color[2], color[3])
        self.vertices = [Vector.Zero()]
        self.mode = GL_POINTS
        self.num_points = 1


class Square(Shape):
    """
    A square image of a single color.
    """

    def __init__(self, color: Sequence[int]):
        super().__init__(color)
        self.vertices = [
            Vector(-1 / 2, 1 / 2),
            Vector(1 / 2, 1 / 2),
            Vector(1 / 2, -1 / 2),
            Vector(-1 / 2, -1 / 2),
        ]

        self.mode = GL_QUADS
        self.num_points = 4


class OutLinedSquare(Square):
    def __init__(self, color: Sequence[int]):
        super().__init__(color)

        self.vertices = [
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
        self.mode = GL_LINES
        self.num_points = 8


class Triangle(Shape):
    """
    A triangle image of a single color.
    """

    def __init__(self, color: Sequence[int]):
        super(Triangle, self).__init__(color)
        self.num_points = 3
        self.vertices = [
            Vector(0, 1 / 2),
            Vector(1 / 2, -1 / 2),
            Vector(-1 / 2, -1 / 2),
        ]
        self.mode = GL_TRIANGLES


class OutlinedTriangle(Triangle):
    def __init__(self, color: Sequence[int]):
        super().__init__(color)
        self.vertices = [
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
        self.num_points = 6
        self.mode = GL_LINES


class Circle(Shape):
    """
    A circle image of a single color.
    """

    def __init__(self, color: Sequence[int], radius=1 / 2):
        super().__init__(color)
        self.center = Vector(0, 0)
        self.radius = radius
        self.mode = GL_TRIANGLE_FAN
        self.num_points = 20


class OutlinedCircle(Circle):
    def __init__(self, color: Sequence[int]):
        super().__init__(color)
        self.mode = GL_LINE_STRIP


class SpriteRenderer(BaseComponent):
    """
    A component that holds the visual information of a sprite
    """

    def __init__(self, entity):
        super().__init__(entity)

        self._image = None  # type: Union[Image, None]
        self._sprite = None  # type: Union[None, pyglet.sprite.Sprite]

        # generate shape
        random.seed(str(self.entity.name))
        r = random.randint(65, 255)
        g = random.randint(65, 255)
        b = random.randint(65, 255)
        a = random.randint(65, 255)
        self.shape = Square((r, g, b, a))

        # size of the sprite
        self._w, self._h = DEFAULT_SPRITE_RESOLUTION[0] * abs(self.entity.transform.scale.x), \
                           DEFAULT_SPRITE_RESOLUTION[1] * abs(self.entity.transform.scale.y)

    def draw_shape(self, batch: "pyglet.graphics.Batch", camera: "kge.Camera", group):
        scale = self.entity.transform.scale
        vertices = []
        if isinstance(self.shape, (Triangle, Square)):
            for v in self.shape.vertices:
                vertices.extend(
                    tuple(camera.world_to_screen_point((self.entity.transform * Vector(v.x * scale.x, v.y * scale.y))))
                )

        elif isinstance(self.shape, Circle):
            deg = 360 / self.shape.num_points
            deg = math.radians(deg)
            for i in range(self.shape.num_points):
                n = deg * i
                vertices.extend((
                    int(self.shape.radius * camera.pixel_ratio * math.cos(n)) + camera.world_to_screen_point(
                        self.entity.position).x,
                    int(self.shape.radius * camera.pixel_ratio * math.sin(n)) + camera.world_to_screen_point(
                        self.entity.position).y
                ))
        else:
            return

        # Add to Batch for drawing
        v_list = batch.add(self.shape.num_points, self.shape.mode, group, ("v2f/dynamic", tuple(vertices)),
                           ("c4Bn/dynamic",
                            self.shape.color * self.shape.num_points))  # type: pyglet.graphics.vertexdomain.VertexList

    def draw_poly(self, Transform: Vector, shape: "Shape", batch: "pyglet.graphics.Batch"):
        # TODO
        pass

    def draw_circle(self, pos: Vector, radius: float, group, color: Tuple[int, int, int],
                    batch: "pyglet.graphics.Batch"):
        # TODO
        pass

    def on_asset_loaded(self, ev: events.AssetLoaded, dispatch):
        """
        If Image has been loaded for this entity then, create the sprite for it
        """
        if isinstance(ev.asset, Image):
            if self._image is not None:
                # Load the asset if it has the same name as self
                if ev.asset.name == self._image.name and self._sprite is None:
                    # print(f'Loading Sprite... for {self.entity}\n')
                    try:
                        self._sprite = pyglet.sprite.Sprite(self._image.load(), subpixel=True)
                        pass
                    except Exception as e:
                        import traceback
                        # print(f"Error : {e}")
                        traceback.print_exc()
                    else:
                        # print(f"Asset loaded ==> {ev.asset.name} {self._image.name} Yes !\n")
                        pass

    @property
    def width(self):
        if self._sprite is not None:
            # If sprite has been loaded
            # Removed !
            # try:
            #     im = self._image.load()  # type: pyglet.image.AbstractImage
            #
            # except Exception as e:
            #     import traceback
            #     # If image has not been loaded yet
            #     print(f"An Error '{e}' Happened on entity {self.entity}")
            #     # traceback.print_exc()
            #     return self._w / DEFAULT_PIXEL_RATIO
            # else:
            #     return im.width / DEFAULT_PIXEL_RATIO
            return self._sprite.image.width / DEFAULT_PIXEL_RATIO
        else:
            return self._w / DEFAULT_PIXEL_RATIO

    @property
    def height(self):
        if self._sprite is not None:
            # If sprite has been loaded
            # Removed !
            # try:
            #     im = self._image.load()  # type: pyglet.image.AbstractImage
            #
            # except Exception as e:
            #     # If image has not been loaded yet
            #     print(f"An Error '{e}' Happened on entity {self.entity}")
            #     return self._h / DEFAULT_PIXEL_RATIO
            # else:
            #     return im.height / DEFAULT_PIXEL_RATIO
            return self._sprite.image.width / DEFAULT_PIXEL_RATIO
        else:
            return self._h / DEFAULT_PIXEL_RATIO

    @property
    def image(self):
        return self._image

    def on_init(self, ev, _):
        pass
        # Removed !
        # try:
        #     self._sprite = pyglet.sprite.Sprite(self._image.load(), subpixel=True)
        # except Exception as e:
        #     # If image has not been loaded yet
        #     print(f"An Error '{e}' Happened on entity {self.entity}")

    @image.setter
    def image(self, val):
        if not isinstance(val, (Image, Shape)):
            raise TypeError(f"image should be of type 'kge.Image' or 'kge.Shape'")

        if isinstance(val, Image):
            self._image = val
        else:
            self.shape = val

    def render(self, scene: "kge.Scene", batch: "pyglet.graphics.Batch", group: "pyglet.graphics.OrderedGroup"):
        """
        Render the sprite
        """
        if self.entity is None or not isinstance(self.entity, kge.Sprite):
            raise AttributeError("Sprite renderer components should be attached to Sprites ('kge.Sprite')")
        else:
            # get camera
            camera = scene.main_camera

            # values
            pos = camera.world_to_screen_point(self.entity.position)

            if self._image is None:
                self.draw_shape(batch, camera, group)
            else:
                # try:
                if self._sprite is None:
                    self.draw_shape(batch, camera, group)
                else:
                    self._sprite.batch = batch
                    self._sprite.group = group
                    self._sprite.update(pos.x, pos.y, self.entity.transform.angle,
                                        scale_x=self.entity.transform.scale.x * camera.zoom,
                                        scale_y=self.entity.transform.scale.y * camera.zoom,
                                        )
            # except Exception as e:
            #     print(f"An Error '{e}' Happened on entity {self.entity}")
            #     # If image has not finished loading yet
