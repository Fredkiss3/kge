import math
import platform
import random
import sys
from typing import Union, Sequence, Optional

import pyglet
from pyglet.gl import *

import kge
from kge.core import events
from kge.core.constants import (
    DEFAULT_SPRITE_RESOLUTION,
    DEFAULT_PIXEL_RATIO, REFERENCE_PIXEL_RATIO)
from kge.graphics.image import Image
from kge.graphics.render_component import RenderComponent
from kge.graphics.shapes import Shape, Circle, Square, Triangle
from kge.utils.color import Color
from kge.utils.vector import Vector

if sys.platform == "win32":
    if platform.architecture()[0] == "64bit":
        import kge.extra.win64.Box2D as b2
    elif platform.architecture()[0] == "32bit":
        import kge.extra.win32.Box2D as b2
else:
    import kge.extra.linux64.Box2D as b2


def make_pixelated(sprite: pyglet.sprite.Sprite):
    """ Make the group of this sprite pixelated.

    :param sprite: pyglet.sprite.Sprite
    :return: None
    """
    import types

    def set_state(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)
        glPushAttrib(GL_COLOR_BUFFER_BIT)
        glEnable(GL_BLEND)
        glTexParameteri(self.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glBlendFunc(self.blend_src, self.blend_dest)

    group = sprite._group
    group.set_state = types.MethodType(set_state, group)


class SpriteRenderer(RenderComponent):
    """
    A component that holds the visual information of a sprite
    """

    # Circle Cache
    circle_segments = 40
    circle_cache_tf = {}  # triangle fan (inside)
    circle_cache_ll = {}  # line loop (border)

    def __init__(self, entity):
        super().__init__(entity)

        # Sprite attributes
        self._next_image = None  # type: Union[Image, None]
        self._image = None  # type: Union[Image, None]
        self._sprite = None  # type: Union[pyglet.sprite.Sprite, None]

        # Color
        self._color = None  # type: Optional[Color]
        self._visible = True

        # generate shape
        random.seed(str(self.entity.name))
        r = random.randint(65, 255)
        g = random.randint(65, 255)
        b = random.randint(65, 255)
        a = random.randint(65, 255) / 255

        # Shape Color & Opacity (Temporary...)
        self._shape_color = Color(r, g, b, a)
        self.shape = Square()

        # Vertex List (if shape)
        self._vlist = None  # type: Optional[pyglet.graphics.vertexdomain.VertexList]

        # size of the sprite
        self._w = DEFAULT_SPRITE_RESOLUTION[0] * \
                  abs(self.entity.transform.scale.x)
        self._h = DEFAULT_SPRITE_RESOLUTION[1] * \
                  abs(self.entity.transform.scale.y)

        self._t = b2.b2Transform()
        self._scale = 0
        # TODO : IS IT PERFORMANT ?
        self._changed = False

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

    def getCircleVertices(self, camera: 'kge.Camera', center, radius, points, solid=True):
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
            if solid:
                self.circle_cache_tf[radius] = self._getTFCircleVertices(radius, points)
            else:
                self.circle_cache_ll[radius] = self._getLLCircleVertices(radius, points)

        vertices = []

        if solid:
            for x, y in self.circle_cache_tf[radius]:
                vertices.extend(
                    (camera.world_to_screen_point(Vector(x + center[0], y + center[1]), ))
                )
        else:
            for x, y in self.circle_cache_ll[radius]:
                vertices.extend(
                    (camera.world_to_screen_point(Vector(x + center[0], y + center[1]), ))
                )
        return vertices

    def draw_shape(self, camera: "kge.Camera"):
        """
        Draw a placeholder shape for the sprite
        """
        scale = self.entity.transform.scale
        vertices = []

        # Default Values when color not specified
        if self._color is not None:
            color = self._color
        else:
            color = self._shape_color

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
                                                       tuple(color) * self.shape.num_points))
            self._vlist.draw(self.shape.mode)
            return self._vlist, self.shape.mode

            # FIXME: THIS DOES NOT WORK PROPERLY
            # if self.shape.radius is None:
            #     self.shape.radius = max(
            #         self.entity.scale.x, self.entity.scale.y) / 2
            #
            # # real world position
            # pos = self.entity.position
            #
            # solid = not isinstance(self.shape, OutlinedCircle)
            # vertices = self.getCircleVertices(camera,
            #                                   pos,
            #                                   self.shape.radius,
            #                                   self.circle_segments,
            #                                   solid
            #                                   )
            #
            # self.shape.num_points = len(vertices) // 2

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
                                     tuple(
                                         color) * self.shape.num_points))  # type: pyglet.graphics.vertexdomain.VertexList
        else:
            # Update vertices
            self._vlist.vertices = vertices
            self._vlist.colors = (*color,) * self.shape.num_points

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

    def delete(self):
        """
        Delete the renderer
        """
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
            if self._sprite is not None:
                self._sprite.image = self._image.load()
            else:
                self._sprite = pyglet.sprite.Sprite(
                    img=self._image.load(), subpixel=True,
                    group=layers[self.entity.layer]
                )

            # Make the sprite pixelated
            make_pixelated(self._sprite)

            # Set debuggable
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
            # Set image only if next image is different
            if self._image != val:
                self._next_image = val
                # TODO : IS IT PERFORMANT ?
                self._changed = True
        else:
            self.shape = val
            # TODO : IS IT PERFORMANT ?
            self._changed = True

    @property
    def opacity(self):
        return self._shape_color.alpha if self._color is None else self._color.alpha

    @opacity.setter
    def opacity(self, val: float):
        if not isinstance(val, (float, int)):
            raise TypeError("Sprite Opacity should be a float between 0 and 1")
        else:
            if not 0 <= val <= 1:
                raise ValueError("Sprite Opacity should be a float between 0 and 1")

            if self._color is None:
                self._color = Color(self._shape_color.red, self._shape_color.green, self._shape_color.blue, val)
                # TODO : IS IT PERFORMANT ?
                self._changed = True
            else:
                if val != tuple(self._color)[:3]:
                    self._color.alpha = val
                    # TODO : IS IT PERFORMANT ?
                    self._changed = True


    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, val: bool):
        if not isinstance(val, (bool)):
            raise TypeError("Sprite Visible Attribute should be a boolean")

        self._visible = val
        # TODO : IS IT PERFORMANT ?
        self._changed = True


    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val: Union[Sequence[int], Color]):
        val = tuple(val)
        if not len(val) >= 3:
            raise IndexError(
                "Too little arguments for Sprite color !\n should be a tuple of integers in form : (red, green, blue), example: (255, 255, 225)")

        r, g, b = val[:3]

        if self._color is None:
            self._color = Color(r, g, b, 1)
            self._color.alpha = self._shape_color.alpha
            # TODO : IS IT PERFORMANT ?
            self._changed = True
        else:
            if val != tuple(self._color)[:3]:
                self._color.red = r
                self._color.green = g
                self._color.blue = b
                # TODO : IS IT PERFORMANT ?
                self._changed = True

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
                # Do not do anything if i'm not in frame
                rb = self.entity.getComponent(kind=kge.RigidBody)
                if rb is not None and (self._sprite is not None or self._vlist is not None):
                    if rb.body_type == kge.RigidBodyType.DYNAMIC:
                        if not camera.in_frame(self.entity, offset=1):
                            self._sprite.visible = False
                            return
                        else:
                            if self._sprite is not None:
                                if self.visible:
                                    self._sprite.visible = True

                if self._next_image is not None:
                    self.set_image()
                    pass
                else:
                    # Check For transform, do not do anything if the entity has not moved
                    t = self.entity.transform.t
                    if self._t.position != t.position \
                            or self._t.angle != t.angle\
                            or self._scale != self.entity.transform.scale\
                            or self._changed:
                        self._t.position = *t.position,
                        self._t.angle = t.angle
                        self._scale = self.entity.transform.scale
                        # TODO : IS IT PERFORMANT ?
                        self._changed = False
                    else:
                        return

                shape = None
                if self._sprite is None:
                    if not self._visible:
                        if self._vlist is not None:
                            self._vlist.delete()
                            self._vlist = None
                    else:
                        shape = self.draw_shape(camera)
                        pass
                else:
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

                        ratio = DEFAULT_PIXEL_RATIO / REFERENCE_PIXEL_RATIO

                        self._sprite.update(pos.x, pos.y, -self.entity.transform.angle,
                                            scale_x=self.entity.transform.scale.x * ratio,
                                            scale_y=self.entity.transform.scale.y * ratio,
                                            )

                # Remove From 'dirties' only if it not a dynamic RigidBody
                dirty = False
                rb = self.entity.getComponent(kind=kge.RigidBody)
                if rb is not None and (self._sprite is not None or self._vlist is not None):
                    if rb.body_type == kge.RigidBodyType.DYNAMIC:
                        dirty = True

                # mark/unmark as dirty
                self.entity.dirty = dirty
                return shape
