from typing import Tuple, Union, Optional, Sequence

import math
import pyglet

import kge
from kge.core.constants import WHITE, DEFAULT_PIXEL_RATIO
from kge.graphics.image import Image
from kge.graphics.shapes import Shape, Circle, Square, Triangle, OutlinedCircle
from kge.graphics.sprite_renderer import make_pixelated
from kge.ui.ui_element import UIElement
from kge.utils.color import Color
from kge.utils.vector import Vector


class Panel(UIElement):
    """
    A panel is just a blank square plane,
    you should use this to add a static image
    or just flat shape to your ui.
    """

    circle_segments = 40
    circle_cache_tf = {}  # triangle fan (inside)
    circle_cache_ll = {}  # line loop (border)

    def __init__(self,
                 img: Union[Image, Shape] = Square(),
                 color: Tuple[int, int, int] = WHITE,
                 opacity: float = 1,
                 ):
        super().__init__()

        # Sprite attributes
        self._next_image = None  # type: Union[Image, None]
        self._image = None  # type: Union[Image, None]
        self._sprite = None  # type: Union[pyglet.sprite.Sprite, None]

        # Color
        self._color = None  # type: Optional[Color]
        self._visible = True

        # Shape Color & Opacity (Temporary...)
        self.shape = Square()

        # Vertex List (if shape)
        self._vlist = None  # type: Optional[pyglet.graphics.vertexdomain.VertexList]

        # Set properties
        self.color = color
        self.image = img
        self.opacity = opacity

    def _getLLCircleVertices(self, radius, points):
        """
        Get the line loop-style vertices for a given circle.
        Drawn as lines.

        "Line Loop" is used as that's how the C++ code draws the
        vertices, with lines going around the circumference of the
        circle (GL_LINE_LOOP).

        This returns 'points' amount of lines approximating the
        border of a circle.

        (x1, y1, x2, y2, x3, y3, ...)
        """
        ret = []
        step = 2 * math.pi / points
        n = 0
        for i in range(points):
            ret.append((math.cos(n) * radius, math.sin(n) * radius))
            n += step
            ret.append((math.cos(n) * radius, math.sin(n) * radius))
        return ret

    def _getTFCircleVertices(self, radius, points):
        """
        Get the triangle fan-style vertices for a given circle.
        Drawn as triangles.

        "Triangle Fan" is used as that's how the C++ code draws the
        vertices, with triangles originating at the center of the
        circle, extending around to approximate a filled circle
        (GL_TRIANGLE_FAN).

        This returns 'points' amount of lines approximating the
        circle.

        (a1, b1, c1, a2, b2, c2, ...)
        """
        ret = []
        step = 2 * math.pi / points
        n = 0
        for i in range(points):
            ret.append((0.0, 0.0))
            ret.append((math.cos(n) * radius, math.sin(n) * radius))
            n += step
            ret.append((math.cos(n) * radius, math.sin(n) * radius))
        return ret

    def getCircleVertices(self, camera: 'kge.Camera', center, radius, points):
        """
        Returns the triangles that approximate the circle and
        the lines that border the circles edges, given
        (center, radius, points).

        Caches the calculated LL/TF vertices, but recalculates
        based on the center passed in.

        Currently, there's only one point amount,
        so the circle cache ignores it when storing. Could cause
        some confusion if you're using multiple point counts as
        only the first stored point-count for that radius will
        show up.

        Returns: (tf_vertices, ll_vertices)
        """
        if radius not in self.circle_cache_tf:
            self.circle_cache_tf[radius] = self._getTFCircleVertices(radius, points)
            self.circle_cache_ll[radius] = self._getLLCircleVertices(radius, points)

        ret_tf, ret_ll = [], []

        for x, y in self.circle_cache_tf[radius]:
            ret_tf.extend(
                (self.rel_pos(camera, Vector(x + center[0], y + center[1]), ))
            )
        for x, y in self.circle_cache_ll[radius]:
            ret_ll.extend(
                (self.rel_pos(camera, Vector(x + center[0], y + center[1]), ))
            )
        return ret_tf, ret_ll

    def draw_shape(self, camera: "kge.Camera"):
        vertices = []

        if isinstance(self.shape, (Triangle, Square)):
            for v in self.shape.vertices:
                vertices.extend(
                    tuple(self.rel_pos(camera,
                                       (
                                               self.transform *
                                               Vector(v.x * self.size.x, v.y * self.size.y)
                                       )
                                       )
                          )
                )
        elif isinstance(self.shape, Circle):
            if self.shape.radius is None:
                self.shape.radius = max(self.size.x, self.size.y) / 2

                # real world position
                pos = self.position + self.parent.position

                tf_vertices, ll_vertices = self.getCircleVertices(camera, pos, self.shape.radius,
                                                                  self.circle_segments)
                tf_count, ll_count = len(tf_vertices) // 2, len(ll_vertices) // 2

                if isinstance(self.shape, OutlinedCircle):
                    self.shape.num_points = ll_count
                    vertices = ll_vertices
                else:
                    self.shape.num_points = tf_count
                    vertices = tf_vertices
        else:
            return

        # Add to Batch for drawing
        if self._vlist is None:
            # Get Batch and layers
            win = kge.ServiceProvider.getWindow()
            batch = win.batch
            layers = win.render_layers
            self._vlist = batch.add(self.shape.num_points, self.shape.mode, layers[self.parent.layer],
                                    ("v2d/stream", tuple(vertices)),
                                    ("c4Bn/dynamic",
                                     (*self._color[:],) * self.shape.num_points)
                                    )  # type: pyglet.graphics.vertexdomain.VertexList
        else:
            # Update vertices
            self._vlist.vertices = vertices
            self._vlist.colors = (*self._color,) * self.shape.num_points

    def set_image(self):
        """
        Set Image
        """
        win = kge.ServiceProvider.getWindow()
        layers = win.render_layers

        # if self._next_image != self._image:
        self._image = self._next_image
        self._next_image = None

        # Set Sprite & delete vertices
        self._sprite = pyglet.sprite.Sprite(
            img=self._image.load(), subpixel=True,
            group=layers[self.parent.layer]
        )

        make_pixelated(self._sprite)

        # Set scales
        scale_x = DEFAULT_PIXEL_RATIO / (self._sprite.width / self.size.x)
        scale_y = DEFAULT_PIXEL_RATIO / (self._sprite.height / self.size.y)

        self._sprite.update(
            scale_x=scale_x,
            scale_y=scale_y,
        )

        if self._vlist is not None:
            self._vlist.delete()
            self._vlist = None

    @property
    def angle(self):
        """
        Get angle, in degrees
        """
        return self.transform.angle

    @angle.setter
    def angle(self, value: float):
        """
        Set angle, in degrees
        """
        self.transform.angle = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, val: Union[Image, Shape]):
        if not isinstance(val, (Image, Shape)):
            raise TypeError(
                f"image should be of type 'kge.Image' or 'kge.Shape'")

        if val != self.image:
            if isinstance(val, Image):
                self._next_image = val
            else:
                self.shape = val

            # Append to render list
            self.append_to_render_list()

    @property
    def opacity(self):
        return self._color.alpha

    @opacity.setter
    def opacity(self, val: float):
        if not isinstance(val, (float, int)):
            raise TypeError("Sprite Opacity should be a float between 0 and 1")
        else:
            if not 0 <= val <= 1:
                raise ValueError("Sprite Opacity should be a float between 0 and 1")

            if self._color is None:
                self._color = Color(*WHITE[:3])
            self._color.alpha = val

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, val: bool):
        if not isinstance(val, (bool)):
            raise TypeError("Sprite Visible Attribute should be a boolean")

        self._visible = val

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val: Union[Sequence[int], Color]):
        val = tuple(val)
        if not isinstance(val, (tuple)):
            raise TypeError(
                "Sprite color should be a tuple of integers in form : (red, green, blue), example: (255, 255, 225)")

        if not len(val) >= 3:
            raise IndexError(
                "Too little arguments for Sprite color !\n should be a tuple of integers in form : (red, green, blue), example: (255, 255, 225)")

        r, g, b = val[:3]

        self._color = Color(r, g, b)

    def delete(self):
        """
        Delete vertices & Sprite if they have been initialized
        :return:
        """
        if self._sprite is not None:
            self._sprite.delete()
            self._sprite = None
        if self._vlist is not None:
            self._vlist.delete()
            self._vlist = None

    def render(self, scene: "kge.Scene"):
        """
        Render the sprite
        """
        # get camera
        camera = scene.main_camera
        win = kge.ServiceProvider.getWindow()
        batch = win.batch

        # values
        pos = self.screen_position(camera)

        # Set Image
        if self._next_image is not None:
            self.set_image()

        # Set image after it has been deleted
        elif self._sprite is None and self._image is not None:
            self._next_image = self._image
            self.set_image()

        # Draw
        if self._sprite is None:
            if not self._visible:
                self.delete()
            else:
                self.draw_shape(camera)
        else:
            # FIXME : IS IT NECESSARY ?
            if not self._visible:
                if self._sprite.batch is not None:
                    self._sprite.batch = None
            else:
                if self._sprite.batch is None:
                    self._sprite.batch = batch

                if self._color is not None and self._sprite.opacity != self._color[-1]:
                    self._sprite.opacity = self._color[-1]

                if self._color is not None and self._sprite.color != tuple(self._color):
                    self._sprite.color = self._color[:3]

                self._sprite.update(pos.x, pos.y,
                                    -self.transform.angle,
                                    )
