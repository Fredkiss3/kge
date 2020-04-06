import random
from typing import Union, Sequence, Optional

import math
import pyglet
from pyglet.gl import *

import kge
from kge.core import events
from kge.core.constants import (
    DEFAULT_SPRITE_RESOLUTION,
    DEFAULT_PIXEL_RATIO, WHITE)
from kge.graphics.image import Image
from kge.graphics.render_component import RenderComponent
from kge.utils.vector import Vector


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
    """
    An outlined square of a single color.
    """

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

    def __init__(self, color: Sequence[int], radius=None):
        super().__init__(color)
        self.center = Vector(0, 0)
        self.radius = radius
        self.mode = GL_TRIANGLE_FAN
        self.num_points = 22


class OutlinedCircle(Circle):
    def __init__(self, color: Sequence[int], radius=1 / 2):
        super().__init__(color, radius)
        self.mode = GL_LINE_LOOP


class SpriteRenderer(RenderComponent):
    """
    A component that holds the visual information of a sprite
    """

    def __init__(self, entity):
        super().__init__(entity)

        # Sprite attributes
        self._next_image = None  # type: Union[Image, None]
        self._image = None  # type: Union[Image, None]
        self._sprite = None  # type: Union[pyglet.sprite.Sprite, None]

        # Color
        self._color = WHITE
        self._opacity = 255
        self._visible = True

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
        self._w = DEFAULT_SPRITE_RESOLUTION[0] * \
                  abs(self.entity.transform.scale.x)
        self._h = DEFAULT_SPRITE_RESOLUTION[1] * \
                  abs(self.entity.transform.scale.y)

    def draw_shape(self, camera: "kge.Camera"):
        scale = self.entity.transform.scale
        vertices = []
        if isinstance(self.shape, (Triangle, Square)):
            for v in self.shape.vertices:
                vertices.extend(
                    tuple(camera.world_to_screen_point(
                        (self.entity.transform * Vector(v.x * scale.x, v.y * scale.y))))
                )
        elif isinstance(self.shape, Circle):
            if self.shape.radius is None:
                self.shape.radius = max(
                    self.entity.scale.x, self.entity.scale.y) / 2
            deg = 360 / self.shape.num_points
            rad = math.radians(deg)
            for i in range(self.shape.num_points):
                n = rad * i
                pos = camera.world_to_screen_point(self.entity.position)
                vertices.extend((
                    int(camera.unit_to_pixels(self.shape.radius)
                        * math.cos(n)) + pos.x,
                    int(camera.unit_to_pixels(self.shape.radius)
                        * math.sin(n)) + pos.y
                ))
            self._vlist = pyglet.graphics.vertex_list(self.shape.num_points,
                                                      ("v2d/stream",
                                                       tuple(vertices)),
                                                      ("c4Bn/dynamic",
                                                       self.shape.color * self.shape.num_points))
            # self._vlist.draw(self.shape.mode)
            return self._vlist, self.shape.mode
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

    def on_disable_entity(self, ev: events.DisableEntity, dispatch):
        """
        Disable sprite if not visible
        """
        if self._vlist is not None:
            self._vlist.delete()
            self._vlist = None
        if self._sprite is not None:
            self._sprite.delete()
            self._sprite = None

    def on_enable_entity(self, ev: events.EnableEntity, dispatch):
        if self._sprite is not None:
            if not self._sprite.visible:
                self._sprite.visible = True

    def on_destroy_entity(self, ev: events.DestroyEntity, dispatch):
        """
        Delete sprite if entity is being deleted
        """
        if self._vlist is not None:
            self._vlist.delete()
            self._vlist = None
        if self._sprite is not None:
            self._sprite.delete()
            self._sprite = None

    def on_scene_stopped(self, ev: events.SceneStopped, dispatch):
        super(SpriteRenderer, self).on_scene_stopped(ev, dispatch)
        if self._vlist is not None:
            self._vlist.delete()
            self._vlist = None
        if self._sprite is not None:
            self._sprite.delete()
            self._sprite = None

    def set_image(self):
        """
        Set Image
        """
        win = kge.ServiceProvider.getWindow()
        layers = win.render_layers

        if self._next_image != self._image:
            self._image = self._next_image
            self._next_image = None

            # Set Sprite & delete vertices
            self._sprite = pyglet.sprite.Sprite(
                img=self._image.load(), subpixel=True,
                group=layers[self.entity.layer]
            )

            if self._vlist is not None:
                self._vlist.delete()
                self._vlist = None

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

    @image.setter
    def image(self, val):
        if not isinstance(val, (Image, Shape)):
            raise TypeError(
                f"image should be of type 'kge.Image' or 'kge.Shape'")

        if isinstance(val, Image):
            self._next_image = val
        else:
            self.shape = val

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, val: float):
        if not isinstance(val, (float, int)):
            raise TypeError("Sprite Opacity should be a float between 0 and 1")
        else:
            if not 0 <= val <= 1:
                raise ValueError("Sprite Opacity should be a float between 0 and 1")

            self._opacity = val * 255

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, val: bool):
        if not isinstance(val, (bool)):
            raise TypeError("Sprite Visible Attribute should be a boolean")

        self._visible = val

    def render(self, scene: "kge.Scene", ):
        """
        Render the sprite
        """
        if self.entity.is_active:
            # get camera
            camera = scene.main_camera
            win = kge.ServiceProvider.getWindow()
            batch = win.batch
            # values
            pos = camera.world_to_screen_point(self.entity.position)

            if self.entity is None or not isinstance(self.entity, kge.Sprite):
                raise AttributeError(
                    "Sprite renderer components should be attached to Sprites ('kge.Sprite')")
            else:
                if self._next_image is not None:
                    self.set_image()

                if not camera.in_frame(self.entity):
                    # FIXME : CAMERA CULLING DROP THE FRAME RATE FOR SPRITES (... WEIRD :( )
                    # If not in camera sight then the sprite should be invisible
                    if self._sprite is not None and self._sprite.batch is not None:
                        # self._sprite.visible = False
                        self._sprite.batch = None
                    else:
                        # If vertex list is not in camera sight then we should delete it
                        if self._vlist is not None:
                            self._vlist.delete()
                            self._vlist = None
                else:
                    if self._sprite is None:
                        if not self._visible:
                            if self._vlist is not None:
                                self._vlist.delete()
                                self._vlist = None
                            return None
                        else:
                            return self.draw_shape(camera)
                    else:
                        if not self._visible:
                            if self._sprite.batch is not None:
                                self._sprite.batch = None
                        else:
                            if self._sprite.batch is None:
                                self._sprite.batch = batch

                            if self._sprite.opacity != self._opacity:
                                self._sprite.opacity = self._opacity

                            if self._sprite.color != tuple(self._color[:3]):
                                self._sprite.color = tuple(self._color[:3])

                            self._sprite.update(pos.x, pos.y, -self.entity.transform.angle,
                                                scale_x=self.entity.transform.scale.x * camera.zoom,
                                                scale_y=self.entity.transform.scale.y * camera.zoom,
                                                )

                        return None
