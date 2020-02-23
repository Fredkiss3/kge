import random
from typing import Union, Sequence, Tuple, Optional

import math
import pyglet
from pyglet.gl import *

import kge
from kge.core import events
from kge.resources.events import AssetLoaded
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
        self.mode = GL_TRIANGLE_STRIP
        self.num_points = 21


class OutlinedCircle(Circle):
    def __init__(self, color: Sequence[int], radius=1 / 2):
        super().__init__(color, radius)
        self.mode = GL_LINES


import decimal


def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        start += decimal.Decimal(str(step))


# if __name__ == '__main__':
#     print(len(list(float_range(0, 2*math.pi, 0.1))))

class SpriteRenderer(BaseComponent):
    """
    TODO : Create properties for color, opacity and tint
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

        # Vertex List (if shape)
        self._vlist = None  # type: Optional[pyglet.graphics.vertexdomain.VertexList]

        # size of the sprite
        self._w, self._h = DEFAULT_SPRITE_RESOLUTION[0] * abs(self.entity.transform.scale.x), \
                           DEFAULT_SPRITE_RESOLUTION[1] * abs(self.entity.transform.scale.y)

    def draw_shape(self, camera: "kge.Camera"):
        # FIXME : SHOULD UPDATE VERTEX LIST IF IT HAS BEEN CREATED
        scale = self.entity.transform.scale
        vertices = []
        if isinstance(self.shape, (Triangle, Square)):
            for v in self.shape.vertices:
                vertices.extend(
                    tuple(camera.world_to_screen_point(
                        (self.entity.transform * Vector(v.x * scale.x, v.y * scale.y))))
                )

        elif isinstance(self.shape, Circle):
            # if not isinstance(self.shape, OutlinedCircle):
            #     # for( float ang=0; ang <= 2*PI; ang += 0.1)
            #     # {
            #     #
            #     # // draw the vertices required.
            #     # glVertex3f(cos(ang)*rad, sin(ang)*rad, 0);
            #     #
            #     # }
            #     # angle = 0
            #     for angle in float_range(0, 2*math.pi, 0.1):
            #         vertices.extend((
            #                 math.cos(angle) * self.shape.radius,
            #                 math.sin(angle) * self.shape.radius,
            #             ))
            #         # angle += 0.1

            # FIXME : CHANGE THIS TO EFFECTIVELY DRAW CIRCLES
            deg = 360 / self.shape.num_points
            rad = math.radians(deg)
            for i in range(self.shape.num_points):
                n = rad * i
                pos = camera.world_to_screen_point(self.entity.position)
                vertices.extend((
                    int(camera.unit_to_pixels(self.shape.radius) * math.cos(n)) + pos.x,
                    int(camera.unit_to_pixels(self.shape.radius) * math.sin(n)) + pos.y
                ))
        else:
            return

        # Add to Batch for drawing
        if self._vlist is None:
            # Get Batch and layers
            win = kge.ServiceProvider.getWindow()
            batch = win.batch
            layers = win.render_layers
            self._vlist = batch.add(self.shape.num_points, self.shape.mode, layers[self.entity.layer],
                                    ("v2d/stream", tuple(vertices)),
                                    ("c4Bn/dynamic",
                                     self.shape.color * self.shape.num_points))  # type: pyglet.graphics.vertexdomain.VertexList
        else:
            # Update vertices
            self._vlist.vertices = vertices

    def draw_poly(self, Transform: Vector, shape: "Shape", batch: "pyglet.graphics.Batch"):
        # TODO
        pass

    def draw_circle(self, pos: Vector, radius: float, group, color: Tuple[int, int, int],
                    batch: "pyglet.graphics.Batch"):
        # TODO
        pass

    def on_disable_entity(self, ev: events.DisableEntity, dispatch):
        """
        Disable sprite if not visible
        """
        if self._vlist is not None:
            self._vlist.delete()
            self._vlist = None
        if self._sprite is not None:
            if self._sprite.visible:
                self._sprite.visible = False
            # self._sprite = None

    def on_enable_entity(self, ev: events.EnableEntity, dispatch):
        if self._sprite is not None:
            if not self._sprite.visible:
                self._sprite.visible = True
        # else:
        #     try:
        #         if self.

    def on_destroy_entity(self, ev: events.DestroyEntity, dispatch):
        """
        Delete sprite if entity is being deleted
        """
        if self._vlist is not None:
            self._vlist.delete()
            self._vlist = None
        if self._sprite is not None:
            if self._sprite.visible:
                self._sprite.visible = False
            self._sprite = None

    def on_asset_loaded(self, ev: AssetLoaded, dispatch):
        """
        If Image has been loaded for this entity then, create the sprite for it
        """
        if isinstance(ev.asset, Image):
            if self._image is not None:
                # Load the asset if it has the same name as self
                if ev.asset.name == self._image.name and self._sprite is None:
                    # print(f'Loading Sprite... for {self.entity}\n')
                    try:
                        # Get batch & group from window service
                        win = kge.ServiceProvider.getWindow()
                        batch = win.batch
                        layers = win.render_layers

                        self._sprite = pyglet.sprite.Sprite(
                            img=self._image.load(), subpixel=True,
                            batch=batch,
                            group=layers[self.entity.layer]
                        )

                        if self._vlist is not None:
                            # print(self._vlist,
                            #       f"for {self.entity}", "Is being Deleted !")
                            self._vlist.delete()
                            self._vlist = None
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
            return self._sprite.width / DEFAULT_PIXEL_RATIO
        else:
            return self._w / DEFAULT_PIXEL_RATIO

    @property
    def height(self):
        if self._sprite is not None:
            return self._sprite.height / DEFAULT_PIXEL_RATIO
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
            raise TypeError(
                f"image should be of type 'kge.Image' or 'kge.Shape'")

        if isinstance(val, Image):
            self._image = val
        else:
            self.shape = val

    def render(self, scene: "kge.Scene", ):
        """
        Render the sprite
        """
        # get camera
        camera = scene.main_camera

        # values
        pos = camera.world_to_screen_point(self.entity.position)

        if self.entity is None or not isinstance(self.entity, kge.Sprite):
            raise AttributeError(
                "Sprite renderer components should be attached to Sprites ('kge.Sprite')")
        else:

            # if not camera.in_frame(self.entity):
            #     # self.entity.is_active = False
            #
            #     # If not in camera sight then the sprite should be invisible
            #     if self._sprite is not None and self._sprite.visible:
            #         self._sprite.visible = False
            #     else:
            #         # If vertex list is not in camera sight then we should delete it
            #         if self._vlist is not None:
            #             self._vlist.delete()
            #             self._vlist = None
            # else:
            if self._sprite is None:
                self.draw_shape(camera)
            else:
                # if self._sprite.batch is None:
                #     self._sprite.batch = batch
                #     self._sprite.group = group
                self._sprite.visible = True
                self._sprite.update(pos.x, pos.y, self.entity.transform.angle,
                                    scale_x=self.entity.transform.scale.x * camera.zoom,
                                    scale_y=self.entity.transform.scale.y * camera.zoom,
                                    )
        # except Exception as e:
        #     print(f"An Error '{e}' Happened on entity {self.entity}")
        #     # If image has not finished loading yet
