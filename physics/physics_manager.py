import logging
import math
from itertools import chain
from typing import Callable, Union, List, Tuple, Sequence, Optional

# from kge.core.system import System
import Box2D as b2
import pyglet
from pyglet import gl

import kge
from kge.core import events
from kge.core.component_system import ComponentSystem
from kge.core.constants import *
from kge.core.entity import BaseEntity
from kge.core.events import Event
from kge.core.service import Service
from kge.physics.colliders import Collider, CircleCollider, BoxCollider, PolygonCollider, LoopCollider, EdgeCollider, \
    TriangleCollider
from kge.physics.events import CollisionEnter, CollisionExit, CreateBody, BodyCreated, BodyDestroyed, DestroyBody, \
    PhysicsUpdate, CollisionBegin, CollisionEnd
from kge.physics.rigid_body import RigidBody
from kge.utils.vector import Vector


class grBlended(pyglet.graphics.Group):
    """
    This pyglet rendering group enables blending.
    """

    def set_state(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def unset_state(self):
        gl.glDisable(gl.GL_BLEND)


class grPointSize(pyglet.graphics.Group):
    """
    This pyglet rendering group sets a specific point size.
    """

    def __init__(self, size=4.0):
        super(grPointSize, self).__init__()
        self.size = size

    def set_state(self):
        gl.glPointSize(self.size)

    def unset_state(self):
        gl.glPointSize(1.0)


class grText(pyglet.graphics.Group):
    """
    This pyglet rendering group sets the proper projection for
    displaying text when used.
    """
    window = None

    def __init__(self, window=None):
        super(grText, self).__init__()
        self.window = window

    def set_state(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.gluOrtho2D(0, self.window.width, 0, self.window.height)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()

    def unset_state(self):
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)


class DebugDrawer(b2.b2Draw):
    """
    This debug draw class accepts callbacks from Box2D (which specifies what to draw)
    and handles all of the rendering.

    If you are writing your own game, you likely will not want to use debug drawing.
    Debug drawing, as its name implies, is for debugging.
    """
    blended = grBlended()
    circle_segments = 40
    surface = None
    circle_cache_tf = {}  # triangle fan (inside)
    circle_cache_ll = {}  # line loop (border)

    def __init__(self, system: "PhysicsManager"):
        super(DebugDrawer, self).__init__()
        # Draw on top of everything
        self.group = pyglet.graphics.OrderedGroup(MAX_LAYERS)
        self.batch = None  # type: Optional[pyglet.graphics.Batch]
        self.system = system
        self.flags = dict(drawShapes=True,
                          drawJoints=True,
                          drawAABBs=False,
                          # Transform
                          drawCOMs=True,
                          # convertVertices=True,
                          )

    def rebatch(self):
        self.win_batch = kge.ServiceProvider.getWindow().batch
        self.batch = pyglet.graphics.Batch()

    def StartDraw(self):
        self.rebatch()

    def EndDraw(self):
        pass

    def triangle_fan(self, vertices):
        """
        in: vertices arranged for gl_triangle_fan ((x,y),(x,y)...)
        out: vertices arranged for gl_triangles (x,y,x,y,x,y...)
        """
        out = []
        for i in range(1, len(vertices) - 1):
            # 0,1,2   0,2,3  0,3,4 ..
            out.extend(vertices[0])
            out.extend(vertices[i])
            out.extend(vertices[i + 1])
        return len(out) // 2, out

    def line_loop(self, vertices):
        """
        in: vertices arranged for gl_line_loop ((x,y),(x,y)...)
        out: vertices arranged for gl_lines (x,y,x,y,x,y...)
        """
        out = []
        for i in range(len(vertices) - 1):
            # 0,1  1,2  2,3 ... len-1,len  len,0
            out.extend(vertices[i])
            out.extend(vertices[i + 1])

        out.extend(vertices[len(vertices) - 1])
        out.extend(vertices[0])

        return len(out) // 2, out

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

    def getCircleVertices(self, center, radius, points):
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
                self.to_screen((x + center[0], y + center[1]))
            )
        for x, y in self.circle_cache_ll[radius]:
            ret_ll.extend(
                self.to_screen((x + center[0], y + center[1]))
            )
        return ret_tf, ret_ll

    def DrawCircle(self, center, radius, color=None):
        """
        Draw an unfilled circle given center, radius and color.
        """
        unused, ll_vertices = self.getCircleVertices(
            center, radius, self.circle_segments)
        ll_count = len(ll_vertices) // 2

        if color is not None:
            self.batch.add(ll_count, gl.GL_LINES, self.group,
                           ('v2f', ll_vertices),
                           ('c4f', [color.r, color.g, color.b, 1.0] * ll_count))

        # Return vertices
        return ll_vertices

    def DrawSolidCircle(self, center, radius, axis, color):
        """
        Draw an filled circle given center, radius, axis (of orientation) and color.
        """
        tf_vertices, ll_vertices = self.getCircleVertices(
            center, radius, self.circle_segments)
        tf_count, ll_count = len(tf_vertices) // 2, len(ll_vertices) // 2

        self.batch.add(tf_count, gl.GL_TRIANGLES, self.blended,
                       ('v2f', tf_vertices),
                       ('c4f', [0.5 * color.r, 0.5 * color.g, 0.5 * color.b, 0.5] * tf_count))

        self.batch.add(ll_count, gl.GL_LINES, self.group,
                       ('v2f', ll_vertices),
                       ('c4f', [color.r, color.g, color.b, 1.0] * (ll_count)))

        p = Vector(center) + radius * Vector(axis)
        if color is not None:
            self.batch.add(2, gl.GL_LINES, self.group,
                           ('v2f', (center[0], center[1], p[0], p[1])),
                           ('c3f', [1.0, 0.0, 0.0] * 2))

    def DrawPolygon(self, vertices, color=None):
        """
        Draw a wireframe polygon given the world vertices (tuples) with the specified color.
        """
        if len(vertices) == 2:
            vces = [*self.to_screen(vertices[0]), *self.to_screen(vertices[1]), ]
            if color is not None:
                self.batch.add(2, gl.GL_LINES, self.group,
                               ('v2f', vces),
                               ('c3f', [color.r, color.g, color.b] * 2))
            return vces
        else:
            ll_count, ll_vertices = self.line_loop([self.to_screen(v) for v in vertices])
            if ll_count == 0:
                return

            if color is not None:
                self.batch.add(ll_count, gl.GL_LINES, self.group,
                               ('v2f', ll_vertices),
                               ('c4f', [color.r, color.g, color.b, 1.0] * (ll_count)))
            return ll_vertices

    def DrawSolidPolygon(self, vertices, color=None):
        """
        Draw a filled polygon given the world vertices (tuples) with the specified color.
        """
        if len(vertices) == 2:
            p1, p2 = [self.to_screen(v) for v in vertices]
            if color is not None:
                self.batch.add(2, gl.GL_LINES, self.group,
                               ('v2f', (p1[0], p1[1], p2[0], p2[1])),
                               ('c3f', [color.r, color.g, color.b] * 2))

        else:
            tf_count, tf_vertices = self.triangle_fan([self.to_screen(v) for v in vertices])
            if tf_count == 0:
                return

            self.batch.add(tf_count, gl.GL_TRIANGLES, self.blended,
                           ('v2f', tf_vertices),
                           ('c4f', [0.5 * color.r, 0.5 * color.g, 0.5 * color.b, 0.5] * (tf_count)))

            ll_count, ll_vertices = self.line_loop([self.to_screen(v) for v in vertices])

            if color is not None:
                self.batch.add(ll_count, gl.GL_LINES, self.group,
                               ('v2f', ll_vertices),
                               ('c4f', [color.r, color.g, color.b, 1.0] * ll_count))

    def DrawSegment(self, p1, p2, color=None):
        """
        Draw the line segment from p1-p2 with the specified color.
        """
        vces = (*self.to_screen(p1), *self.to_screen(p2))

        if color is not None:
            self.batch.add(2, gl.GL_LINES, self.group,
                           ('v2f', vces),
                           ('c3f', [color.r, color.g, color.b] * 2))
        return vces

    def DrawTransform(self, xf):
        """
        Draw the transform xf on the screen
        """
        p1 = xf.position
        k_axisScale = 0.4
        p2 = p1 + k_axisScale * xf.R.x_axis
        p3 = p1 + k_axisScale * xf.R.y_axis

        p1, p2, p3 = self.to_screen(p1), self.to_screen(p2), self.to_screen(p3),

        vces = (p1[0], p1[1], p2[0], p2[1], p1[0], p1[1], p3[0], p3[1])
        # if color is not None:
        self.batch.add(4, gl.GL_LINES, self.group,
                       ('v2f', vces),
                       ('c3f', [1.0, 0.0, 0.0] * 2 + [0.0, 1.0, 0.0] * 2))
        return vces

    def DrawPoint(self, p, size, color):
        """
        Draw a single point at point p given a point size and color.
        """
        p = self.to_screen(p)
        if color is not None:
            self.batch.add(1, gl.GL_POINTS, grPointSize(size),
                           ('v2f', (p[0], p[1])),
                           ('c3f', [color.r, color.g, color.b]))

    def DrawAABB(self, aabb, color=None):
        """
        Draw a wireframe around the AABB with the given color.
        """
        vces = (
            *self.to_screen((aabb.lowerBound.x, aabb.lowerBound.y)),
            *self.to_screen((aabb.upperBound.x, aabb.lowerBound.y)),
            *self.to_screen((aabb.upperBound.x, aabb.lowerBound.y)),
            *self.to_screen((aabb.upperBound.x, aabb.upperBound.y)),
            *self.to_screen((aabb.upperBound.x, aabb.upperBound.y)),
            *self.to_screen((aabb.lowerBound.x, aabb.upperBound.y)),
            *self.to_screen((aabb.lowerBound.x, aabb.upperBound.y)),
            *self.to_screen((aabb.lowerBound.x, aabb.lowerBound.y)),
        )
        if color is not None:
            self.batch.add(len(vces) // 2, gl.GL_LINES, self.group,
                           ('v2f', vces),
                           ('c3f', [color.r, color.g, color.b] * (len(vces) // 2))
                           )
        return (
            vces
        )

    def to_screen(self, point):
        """
        In here for compatibility with other frameworks.
        """
        cam = self.system.engine.current_scene.main_camera
        return tuple(cam.world_to_screen_point(Vector(*point)))

    def DrawShape(self, col: Collider, xf: b2.b2Transform) -> Tuple[List[int], int, List[int]]:
        """
        Draw a Shape
        """
        color = b2.b2Color(*[c / 255 for c in GREEN[:3]])
        vertices = []
        mode = gl.GL_LINES

        if isinstance(col, CircleCollider):
            center = xf * col.offset
            radius = col.radius
            # axis = xf.q * b2.b2Vec2(1.0, 1.0)

            vertices = self.DrawCircle(center, radius, color)

        elif isinstance(col, (TriangleCollider, PolygonCollider, BoxCollider)):
            count = col.shape.vertexCount
            vces = col.shape.vertices
            assert count <= b2.b2_maxPolygonVertices

            for i in range(count):
                vertices.append(xf * vces[i])

            vertices = self.DrawPolygon(vertices)

        elif isinstance(col, LoopCollider):
            count = col.shape.vertexCount
            vces = col.shape.vertices

            v1 = xf * vces[0]
            for i in range(1, count):
                v2 = xf * vces[i]
                [vertices.append(v) for v in self.DrawSegment(v1, v2)]
                # vertices.append(self.DrawCircle(v1, 0.05))
                v1 = v2

        elif isinstance(col, EdgeCollider):
            v1 = xf * col.shape.vertex1
            v2 = xf * col.shape.vertex2

            vertices = self.DrawSegment(v1, v2)

        colors = [color.r, color.g, color.b] * (len(vertices) // 2)
        return vertices, mode, colors

    def DrawFix(self, fix: b2.b2Fixture, cam: "kge.Camera", xf: b2.b2Transform):
        """
        Draw a Fixture
        """
        col = fix.userData  # type: Collider

        if col is not None:
            if col.fixture is not None:
                if cam.in_frame(col.entity):
                    vertices, mode, colors = self.DrawShape(col, xf)

                    if col.vlist is None:
                        # Add vertices to Batch
                        count = len(vertices) // 2

                        col.vlist = self.win_batch.add(count, mode, self.group,
                                                       ('v2f/stream', vertices),
                                                       ('c3f/dynamic', colors))
                    else:
                        # Update vertices
                        col.vlist.vertices = self.DrawShape(col, xf)[0]
                else:
                    if col.vlist is not None:
                        col.vlist.delete()
                        col.vlist = None

    def DrawBody(self, b: b2.b2Body):
        """
        Draw all a body and its Fixtures
        """
        cam = self.system.engine.current_scene.main_camera
        # transform of the rb
        if b.active:
            rb = b.userData  # type: RigidBody
            if rb is not None:
                if rb.body is not None:
                    xf = rb.body.transform  # type: b2.b2Transform
                    xf.position = rb.position

                    if cam.in_frame(rb.entity):
                        xf_vertices = self.DrawTransform(xf)
                        if rb.vlist is None:
                            # Add vertices to Batch
                            rb.vlist = self.win_batch.add(len(xf_vertices) // 2, gl.GL_LINES, self.group,
                                                          ('v2f/stream', xf_vertices),
                                                          ('c3f/dynamic', [1.0, 0.0, 0.0] * 2 + [0.0, 1.0, 0.0] * 2))
                        else:
                            # Update vertices
                            rb.vlist.vertices = self.DrawTransform(xf)
                    else:
                        if rb.vlist is not None:
                            rb.vlist.delete()
                            rb.vlist = None

                    for f in b.fixtures:
                        self.DrawFix(f, cam, xf)


class ContactListener(b2.b2ContactListener):
    """
    The contact listener of the system
    """

    def __init__(self, system: "PhysicsManager", **kwargs):
        super().__init__(**kwargs)
        self.system = system

    def PreSolve(self, contact, oldManifold):
        self.system.pre_solve(contact)

    def BeginContact(self, contact):
        """
        Trigger Collision Enter functions

        :param contact:
        :return:
        """
        self.system.handle_contact(contact, True)

    def EndContact(self, contact):
        """
        Trigger Collision Exit functions

        :param contact:
        :return:
        """
        self.system.handle_contact(contact, False)

    def PostSolve(self, contact, impulse):
        self.system.post_solve(contact)


class DestructionListener(b2.b2DestructionListener):
    """
    The Destruction listener of the system
    """

    def __init__(self, system: "PhysicsManager", **kwargs):
        super().__init__(**kwargs)
        self.system = system

    def SayGoodbye(self, fixture):
        """
        When a fixture gets destroyed

        :param fixture:
        :return:
        """
        self.system.handle_destruction(fixture)


class OverlapInfo(b2.b2QueryCallback):
    """
    TODO : TO TEST
    """
    MULTIPLE = 1
    ONE = 0

    def __init__(self, type=ONE, layer=None):
        super().__init__()
        self.type = type
        self.colliders = []  # type: List[Collider]
        self.collider = None
        self.layer = layer

    def ReportFixture(self, fixture):
        """
        Called for each fixture found in the query AABB.
        false to terminate the query.
        :param fixture: a fixture found in the query
        :return: True to continue the query, False to terminate the query
        """
        collider = fixture.userData  # type: Collider

        if collider is not None and not isinstance(collider, Collider):
            # We pass through each fixture which is not a collider
            return True
        else:
            if self.layer is not None:
                if self.layer == collider.entity.layer:
                    if self.type == OverlapInfo.ONE:
                        self.collider = collider
                        # Stop
                        return False
                    else:
                        self.colliders.append(collider)
                        # Continue looking for more colliders
                        return True
                else:
                    # Pass Through each collider which is not in the same layer
                    return True
            else:
                if self.type == OverlapInfo.ONE:
                    self.collider = collider
                    # Stop
                    return False
                else:
                    self.colliders.append(collider)
                    # Continue looking for more colliders
                    return True


class RegionInfo(OverlapInfo):
    MULTIPLE = 1
    ONE = 0


class RayCastInfo(b2.b2RayCastCallback):
    CLOSEST = 1
    MULTIPLE = 2
    ANY = 3

    def __init__(self, type=CLOSEST, layer=None, maxPoint: Vector = Vector.Zero()):
        b2.b2RayCastCallback.__init__(self)
        self.collider = None
        self.colliders = []
        self.point = None
        self.normal = None
        self.hit = False
        self.max_point = maxPoint
        self.type = type
        self.points = []
        self.normals = []
        self.layer = layer

    def ReportFixture(self, fixture, point, normal, fraction):
        """
        Called for each fixture found in the query. You control how the ray
        proceeds by returning a float that indicates the fractional length of
        the ray. By returning 0, you set the ray length to zero. By returning
        the current fraction, you proceed to find the closest point. By
        returning 1, you continue with the original ray clipping. By returning
        -1, you will filter out the current fixture (the ray will not hit it).
        """
        collider = fixture.userData  # type: Collider

        if collider is not None and not isinstance(collider, Collider):
            # We pass through each fixture which is not a collider
            return -1

        if self.layer is not None:
            if collider is not None:
                if collider.entity.layer == self.layer:
                    self.hit = True
                    self.collider = collider
                else:
                    # We pass through each collider which is not in this layer
                    return -1
            else:
                # We pass through each fixture which is not a collider
                return -1
        else:
            if collider is not None:
                if self.type == RayCastInfo.MULTIPLE or self.type == RayCastInfo.ANY:
                    self.colliders.append(collider)
                else:
                    self.collider = collider
                self.hit = True
                self.point = Vector(*point)
                self.normal = Vector(*normal)
        # NOTE: You will get this error:
        #   "TypeError: Swig director type mismatch in output value of
        #    type 'float32'"
        # without returning a value

        if self.type == RayCastInfo.CLOSEST:
            return fraction
        elif self.type == RayCastInfo.ANY:
            return 0.0
        elif self.type == RayCastInfo.MULTIPLE:
            if self.hit:
                self.points.append(Vector(*point))
                self.normals.append(Vector(*normal))
            return 1.0


class PhysicsManager(ComponentSystem):
    """
    The system that handles movement, collision detection and can perform region queries and ray casts
    """
    contact_listener: ContactListener = None
    destruction_listener: DestructionListener = None
    world: Union[None, b2.b2World] = None
    pause: bool = False
    engine: "kge.Engine"

    @classmethod
    def ignore_layer_collision(cls, layer1: Union[int, str], layer2: Union[int, str]):
        # TODO
        l1 = cls.engine.current_scene.getLayer(layer1)
        l2 = cls.engine.current_scene.getLayer(layer2)
        raise NotImplementedError("Not implemented Yet !")

    @classmethod
    def overlap_circle(cls, center: Vector, radius: float, layer: Union[int, str, None] = None,
                       type=OverlapInfo.MULTIPLE) -> OverlapInfo:
        """
        Query for colliders which are in a given circle region
        Note: in reality this method does not query in a circle region but a squared region

        :param center: The center point of the circle to overlap
        :param radius: the radius of the circle to overlap
        :param layer: the layer to filter
        :param type: type of overlap. should be one of :
            - OverlapInfo.ONE => The Overlap Function will return only one collider found when overlapping
            - OverlapInfo.MULTIPLE => T The Overlap Function will return only all colliders found when overlapping
        :return: an object of type OverlapInfo, which holds information about the result of the Overlap
            Example of use :
                >>> PhysicsManager.overlap_circle( center=Vector(0, 0), radius=1, type=OverlapInfo.ONE, layer="Ground" )
        """
        # if type in (OverlapInfo.MULTIPLE, OverlapInfo.ONE):
        #     lay = None
        #     if layer is not None:
        #         lay = cls.engine.current_scene.getLayer(layer)
        #     cb = OverlapInfo(type=type, layer=lay)
        #
        #     # Make a small box.
        #     aabb = b2.b2AABB(lowerBound=center - Vector(radius, radius),
        #                      upperBound=center + Vector(radius, radius))
        #
        #     # Query the world for overlapping shapes.
        #     cls.world.QueryAABB(cb, aabb)
        #
        #     return cb
        # else:
        #     raise ValueError(
        #         "Overlap Type should be one of 'OverlapInfo.ONE or OverlapInfo.MULTIPLE'")
        raise NotImplementedError("Not implemented yet !")

    @classmethod
    def query_region(cls, center: Vector, size: Vector, layer: Union[int, str] = None,
                     type=RegionInfo.MULTIPLE) -> RegionInfo:
        """
        Query for colliders which are in a given region

        :param center: the center of the region to query
        :param size: the size (width, height) of the region to query
        :param layer: the layer to filter
        :param type: type of overlap. should be one of :
            - RegionInfo.ONE => The Query Function will return only one collider found when query is finished
            - RegionInfo.MULTIPLE => The Query Function will return all colliders found when query is finished

        :return: an object of type RegionInfo, which holds information about the result of the Query
            Example of use :
                >>> hit = PhysicsManager.query_region(
                >>>                 center=Vector(0, 0),
                >>>                 size=Vector(1, 1),
                >>>                 type=RegionInfo.ONE,
                >>>                 layer="Ground"
                >>> )
                >>> print(hit.collider)
        """
        if type in (RegionInfo.MULTIPLE, RegionInfo.ONE):
            lay = None
            if layer is not None:
                lay = cls.engine.current_scene.getLayer(layer)
            cb = RegionInfo(type=type, layer=lay)

            # Set size corrections
            size = abs(abs(size))

            # Make a small box.
            aabb = b2.b2AABB(lowerBound=center - size / 2,
                             upperBound=center + size / 2)

            if cls.world is not None:
                # Query the world for shapes.
                cls.world.QueryAABB(cb, aabb)

            return cb
        else:
            raise ValueError(
                "Query Type should be one of 'RegionInfo.ONE or RegionInfo.MULTIPLE'")

    @classmethod
    def ray_cast(cls, origin: Vector, direction: Vector, distance: float, layer: Union[int, str, None] = None,
                 type=RayCastInfo.CLOSEST) -> RayCastInfo:
        """
        Perform a ray cast

        :param origin: The origin point of the ray cast
        :param direction: the direction in which we want to launch the ray
        :param distance: the distance of the ray
        :param layer: the layer to filter
        :param type: type of ray cast. should be one of :
            - RayCastInfo.CLOSEST => The ray cast will returns the closest point that the ray touched
            - RayCastInfo.MULTIPLE => The ray cast will returns all the points that the ray touched
            - RayCastInfo.ANY => The ray cast will returns all the points that the ray touched
        :return: an object of type RayCastInfo, which holds information about the result of the ray cast
            Example of use :
                >>> PhysicsManager.ray_cast( origin=Vector(0, 0), direction=Vector(1, 1), distance=12, layer="Ground" )
        """
        if type in (RayCastInfo.MULTIPLE, RayCastInfo.CLOSEST, RayCastInfo.ANY):
            lay = None
            if layer is not None:
                lay = cls.engine.current_scene.getLayer(layer)

            # normalize the direction to make it of magnitude 1
            direction = direction.normalized()

            # Calculate the destination of the ray
            dest = origin + direction * distance
            cb = RayCastInfo(type=type, layer=lay, maxPoint=dest)

            # Send the ray
            if cls.world is not None:
                cls.world.RayCast(cb, origin, (dest.x, dest.y))

            return cb
        else:
            raise ValueError(
                "RayCast Type should be one of 'RayCastInfo.MULTIPLE, RayCastInfo.CLOSEST, RayCastInfo.ANY'")

    def __init__(self, engine, **_):
        """
        TODO : Create And Destroy Joint
        """
        super(PhysicsManager, self).__init__(engine)

        # state
        self.debug_drawer = DebugDrawer(self)
        PhysicsManager.contact_listener = ContactListener(self)
        PhysicsManager.destruction_listener = DestructionListener(self)
        PhysicsManager.engine = self.engine

        # only rigid bodies and colliders supported
        self.components_supported = [RigidBody, Collider]

        # bodies to destroy
        self.garbage_bodies = []  # type: List[b2.b2Body]
        # bodies to create
        self.new_bodies = []  # type: List[Tuple[RigidBody, BaseEntity]]

        # TODO : Implement layers in order to ignore collisions within different layers
        self.layers_to_ignore = {}

    def on_physics_update(self, event: PhysicsUpdate, dispatch: Callable[[Event], None]):
        """
        Update physics
        """
        cls = PhysicsManager
        if not self.pause:
            if cls.world:
                # Disable garbage bodies from being simulated
                for body in self.garbage_bodies:
                    body.active = False
                    # Note: this has been removed because it causes bugs
                    # cls.world.DestroyBody(body)
                self.garbage_bodies.clear()

                # Create new bodies
                for rb, e in self.new_bodies:
                    self.create_body(rb, e)
                self.new_bodies.clear()

                # Update the physics world
                cls.world.Step(
                    FIXED_DELTA_TIME * event.time_scale, 10, 10)
                cls.world.ClearForces()

                # Debug Draw only if debug is activated
                if self.logger.getEffectiveLevel() == logging.DEBUG:
                    self._dispatch(events.DebugDraw())

    def on_debug_draw(self, event: events.DebugDraw, dispatch: Callable[[Event], None]):
        self.debug_drawer.StartDraw()
        cls = PhysicsManager
        # debug = kge.ServiceProvider.getDebug()
        if cls.world:
            if not cls.world.locked:
                cls.world.DrawDebugData()
                # debug.draw_world()
        self.debug_drawer.EndDraw()

    def on_disable_entity(self, event: events.DisableEntity, dispatch: Callable[[Event], None]):
        """
        Disable the rigid body too
        """
        rb = event.entity.getComponent(RigidBody)
        if rb is not None:
            rb.active = False

            ev = events.EntityDisabled(
                entity=event.entity
            )
            ev.onlyEntity = event.entity
            dispatch(ev)

    def on_enable_entity(self, event: events.EnableEntity, dispatch: Callable[[Event], None]):
        """
        Enable the rigid body too
        """
        rb = event.entity.getComponent(RigidBody)
        if rb is not None:
            rb.active = True
            rb.is_active = True

            ev = events.EntityEnabled(
                entity=event.entity
            )
            ev.onlyEntity = event.entity
            dispatch(ev)

    def on_scene_paused(self, ev: events.ScenePaused, dispatch: Callable[[Event], None]):
        self.pause = True

    def on_scene_continued(self, ev: events.SceneContinued, dispatch: Callable[[Event], None]):
        self.pause = False

    def on_scene_started(self, ev: events.SceneStarted, dispatch: Callable[[Event], None]):
        cls = PhysicsManager
        cls.world = b2.b2World(gravity=(0, -10), doSleep=True)
        win = kge.ServiceProvider.getWindow()

        self.debug_drawer.batch = win.batch
        self.debug_drawer.cam = self.engine.current_scene.main_camera

        cls.world.renderer = self.debug_drawer

        cls.world.contactListener = self.contact_listener
        cls.world.destructionListener = self.destruction_listener

    def create_body(self, rb: RigidBody, e: BaseEntity):
        """
        Create the real body
        """
        try:
            # Set position and angle
            rb.angle = e.angle
            body = PhysicsManager.world.CreateBody(
                b2.b2BodyDef(
                    position=e.position,
                    angle=math.radians(rb.angle),
                    type=rb.b_type,
                    active=rb.active,
                    allowSleep=True,
                    awake=True,
                    fixedRotation=rb.fixed_rotation,
                    userData=rb,
                    gravityScale=rb.gravity_scale,
                    bullet=True,
                )
            )  # type: b2.b2Body
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.logger.error(e)
        else:
            # Set mass, velocity and inertia of the body
            body.mass = rb.mass
            body.linearVelocity = rb.velocity
            body.angularVelocity = rb.angular_velocity
            body.linearDamping = rb.drag
            body.inertia = rb.inertia
            body.angle = math.radians(rb.angle)

            # the body has been created
            event = BodyCreated(
                entity=e,
                body=body
            )
            event.onlyEntity = e
            self._dispatch(event)

    def on_create_body(self, ev: CreateBody, dispatch: Callable[[Event], None]):
        """
        Create a body
        """
        rb = ev.body_component
        e = ev.entity

        if rb.is_ghost:
            manager = kge.ServiceProvider.getEntityManager()
            manager.add_component(e, rb)

        self.new_bodies.append((rb, ev.entity))

    def on_body_created(self, event: BodyCreated, dispatch):
        # get the concerned components
        concerned = chain(event.entity.getComponents(kind=RigidBody), event.entity.getComponents(kind=Collider))
        for c in concerned:  # type: Union[RigidBody, Collider]
            c.__fire_event__(event, dispatch)

    def on_body_destroyed(self, event: BodyDestroyed, dispatch):
        # get the concerned components
        concerned = chain(event.entity.getComponents(kind=RigidBody), event.entity.getComponents(kind=Collider))

        for c in concerned:  # type: Union[RigidBody, Collider]
            c.__fire_event__(event, dispatch)
            if c in self._components:
                self._components.remove(c)
                self.unregister_events(c)

    def __exit__(self, exc_type, exc_val, exc_tb):
        PhysicsManager.world = None

    def handle_contact(self, contact: b2.b2Contact, began: bool):
        """
        Handle a contact, it will generate collisions only
        if two colliders have made contact. And it will generate collisions enter & exit events
        only on colliders which are sensors.
        """
        collider_a = contact.fixtureA.userData
        collider_b = contact.fixtureB.userData

        rb_a = contact.fixtureA.body.userData  # type: RigidBody
        rb_b = contact.fixtureB.body.userData  # type: RigidBody

        if isinstance(rb_a, RigidBody) and isinstance(rb_b, RigidBody):
            if rb_a.is_active and rb_b.is_active:
                # enable collision only for active rigid bodies
                if isinstance(collider_a, Collider) and isinstance(collider_b, Collider):
                    if collider_a.isSensor or collider_b.isSensor:
                        if self._dispatch:
                            if began:
                                if collider_b.isSensor:
                                    # generate collision for b
                                    c_ev_a = CollisionEnter(collider=collider_a)
                                    c_ev_a.onlyEntity = collider_b.entity
                                    self._dispatch(c_ev_a)

                                if collider_a.isSensor:
                                    # generate collision for a
                                    c_ev_b = CollisionEnter(collider=collider_b)
                                    c_ev_b.onlyEntity = collider_a.entity
                                    self._dispatch(c_ev_b)
                            else:
                                # generate collision for b
                                if collider_b.isSensor:
                                    c_ev_a = CollisionExit(collider=collider_a)
                                    c_ev_a.onlyEntity = collider_b.entity
                                    self._dispatch(c_ev_a)

                                # generate collision for a
                                if collider_a.isSensor:
                                    c_ev_b = CollisionExit(collider=collider_b)
                                    c_ev_b.onlyEntity = collider_a.entity
                                    self._dispatch(c_ev_b)

                    # if neither of objects are sensors then
                    elif not (collider_a.isSensor and collider_b.isSensor):
                        if began:
                            # generate collision for b
                            c_ev_a = CollisionBegin(collider=collider_a)
                            c_ev_a.onlyEntity = collider_b.entity
                            self._dispatch(c_ev_a)

                            # generate collision for a
                            c_ev_b = CollisionBegin(collider=collider_b)
                            c_ev_b.onlyEntity = collider_a.entity
                            self._dispatch(c_ev_b)
                        else:
                            # generate collision for b
                            c_ev_a = CollisionEnd(collider=collider_a)
                            c_ev_a.onlyEntity = collider_b.entity
                            self._dispatch(c_ev_a)

                            # generate collision for a
                            c_ev_b = CollisionEnd(collider=collider_b)
                            c_ev_b.onlyEntity = collider_a.entity
                            self._dispatch(c_ev_b)
            else:
                # contact.enabled = False
                pass

    def on_entity_destroyed(self, ev: events.EntityDestroyed, dispatch: Callable[[Event, bool], None]):
        rb = ev.entity.getComponent(kind=RigidBody)  # type: RigidBody

        if rb is not None:
            # Disable body
            rb.active = False

            # Then destroy the Body
            event = DestroyBody(
                entity=ev.entity,
                body_component=rb
            )
            event.onlyEntity = ev.entity
            dispatch(event, True)

    def on_destroy_body(self, ev: DestroyBody, dispatch):
        """
        Destroy a body
        """
        if ev.body_component.body is not None:
            while PhysicsManager.world.locked:
                continue

            ev.body_component.is_active = False
            colliders = ev.entity.getComponents(kind=Collider)
            for col in colliders:
                col.is_active = False

            # Put the bodies into garbage collector
            self.garbage_bodies.append(ev.body_component.body)

            # set user data to none in order to free it
            ev.body_component.body.userData = None
            event = BodyDestroyed(
                body=ev.body_component.body,
                entity=ev.entity
            )
            event.onlyEntity = ev.entity
            dispatch(event)

    def handle_destruction(self, fixture: b2.b2Fixture):
        """
        Did a fixture get destroyed ?
        """
        self.logger.info(f"GoodBye... {fixture.userData}")

    def pre_solve(self, contact: b2.b2Contact):
        """
        Pre Solve a contact in order to deactivate contact
        """
        collider_a = contact.fixtureA.userData
        collider_b = contact.fixtureB.userData

        if isinstance(collider_a, Collider) and isinstance(collider_b, Collider):
            # disable contact if one of the colliders is not active
            if not collider_a.is_active or not collider_b.is_active:
                contact.enabled = False
        else:
            contact.enabled = False

    def post_solve(self, contact: b2.b2Contact):
        """
        Not called for sensors
        """

        pass


class Physics(Service):
    system_class = PhysicsManager
    _system_instance: PhysicsManager

    def ray_cast(self, origin: Vector, direction: Vector, distance: float, layer: Union[int, str, None] = None,
                 type=RayCastInfo.CLOSEST) -> RayCastInfo:
        return self._system_instance.ray_cast(origin, direction, distance, layer, type)

    def overlap_circle(self, center: Vector, radius: float, layer: Union[int, str, None] = None,
                       type=OverlapInfo.MULTIPLE) -> OverlapInfo:
        return self._system_instance.overlap_circle(center, radius, layer, type)

    def query_region(self, center: Vector, size: Vector, layer: Union[int, str, None] = None,
                     type=RegionInfo.MULTIPLE) -> RegionInfo:
        return self._system_instance.query_region(center, size, layer, type)

    @property
    def world(self):
        return self._system_instance.world

    @property
    def gravity(self):
        return Vector(self._system_instance.world.gravity[0], self._system_instance.world.gravity[1], )

    @gravity.setter
    def gravity(self, val: Vector):
        if not isinstance(val, Vector):
            raise TypeError("Gravity should be a Vector")

        self._system_instance.world.gravity = val

    @property
    def debug_drawer(self):
        return self._system_instance.debug_drawer


class DebugDrawService(Service):
    """
    The service that helps to draw custom shape and others
    TODO : Custom Draw
    """
    system_class = PhysicsManager
    _system_instance: PhysicsManager

    def __init__(self, instance: PhysicsManager):
        super().__init__(instance)
        self.debug = instance.debug_drawer

    @property
    def flags(self):
        return self._system_instance.debug_drawer.flags

    @flags.setter
    def flags(self, val: dict):
        """
        Get the draw flags
        TODO : Annotate attributes
        """
        if not isinstance(val, dict):
            raise TypeError("Flags should be a dict")
        self._system_instance.debug_drawer.flags = val

    def draw_world(self):
        """
        Draw the world
        FIXME : OPTIMIZE THIS
        """
        # Draw all rigid bodies
        for b in self._system_instance.world:
            self.debug.DrawBody(b)

        # Draw all joints
        # TODO

    def to_screen(self, point: Vector) -> Tuple[float, float]:
        return tuple(self._system_instance.engine.current_scene.main_camera.world_to_screen_point(point))

    def to_pixels(self, unit: float):
        return self._system_instance.engine.current_scene.main_camera.unit_to_pixels(unit)

    def getColor(self, color: Sequence[int]):
        return b2.b2Color([c / 255 for c in color[:3]])

    def draw_circle(self, center: Vector, radius: float, color: Tuple[int, int, int, int], solid=False):
        if not solid:
            self.debug.DrawCircle(center, radius, self.getColor(color))
        else:
            self.debug.DrawSolidCircle(center, radius, Vector.Up(), self.getColor(color))

    def draw_segment(self, p1: Vector, p2: Vector, color: Tuple[int, int, int, int]):
        self.debug.DrawSegment(p1, p2, self.getColor(color))

    def draw_poly(self, vertices: List[Vector], color: Tuple[int, int, int, int], solid=False):
        if not solid:
            self.debug.DrawPolygon(vertices, self.getColor(color))
        else:
            self.debug.DrawSolidPolygon(vertices, self.getColor(color))

    def draw_box(self, center: Vector, size: Vector, color: Tuple[int, int, int, int], solid=False):
        aabb = b2.b2AABB(
            lowerBound=center - size / 2,
            upperBound=center + size / 2,
        )

        if not solid:
            self.debug.DrawAABB(aabb, self.getColor(color))
        else:
            vces = (
                (aabb.lowerBound.x, aabb.lowerBound.y),
                (aabb.upperBound.x, aabb.lowerBound.y),
                (aabb.upperBound.x, aabb.lowerBound.y),
                (aabb.upperBound.x, aabb.upperBound.y),
                (aabb.upperBound.x, aabb.upperBound.y),
                (aabb.lowerBound.x, aabb.upperBound.y),
                (aabb.lowerBound.x, aabb.upperBound.y),
                (aabb.lowerBound.x, aabb.lowerBound.y),
            )
            self.debug.DrawSolidPolygon(vces, self.getColor(color))

    def draw_point(self, p: Vector, size: float, color: Tuple[int, int, int, int]):
        p = self.to_screen(p)
        self.debug.DrawPoint(p, size, color)

    def Print(self, string: str, point: Vector, color=(229, 153, 153, 255)):
        """
        Draw some text, str, at screen coordinates (x, y).
        """
        win = kge.ServiceProvider.getWindow()
        point = self.to_screen(point)
        pyglet.text.Label(string,
                          font_size=15, x=point[0], y=point[1],
                          color=color,
                          batch=self.debug.batch,
                          group=grText(window=win.window)
                          )


if __name__ == '__main__':
    with PhysicsManager(None) as p_m:
        pass
