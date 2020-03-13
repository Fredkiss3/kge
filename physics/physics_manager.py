import logging
import math
from itertools import chain
from typing import Callable, Union, List, Tuple, Sequence

# from kge.core.system import System
import Box2D as b2

import kge
from kge.core import events
from kge.core.component_system import ComponentSystem
from kge.core.constants import *
from kge.core.entity import BaseEntity
from kge.core.events import Event
from kge.core.service import Service
from kge.physics.colliders import Collider
from kge.physics.events import CollisionEnter, CollisionExit, CreateBody, BodyCreated, BodyDestroyed, DestroyBody, \
    PhysicsUpdate, CollisionBegin, CollisionEnd
from kge.physics.rigid_body import RigidBody, RigidBodyType
from kge.utils.vector import Vector

import pyglet
from pyglet import gl


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
    circle_segments = 16
    surface = None
    circle_cache_tf = {}  # triangle fan (inside)
    circle_cache_ll = {}  # line loop (border)

    def __init__(self, system: "PhysicsManager", batch=None):
        super(DebugDrawer, self).__init__()
        self.group = pyglet.graphics.OrderedGroup(21)
        self.batch = batch
        self.system = system

    def StartDraw(self):
        pass

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

        TODO: Currently, there's only one point amount,
        so the circle cache ignores it when storing. Could cause
        some confusion if you're using multiple point counts as
        only the first stored point-count for that radius will
        show up.
        TODO: What does the previous TODO mean?

        Returns: (tf_vertices, ll_vertices)
        """
        if radius not in self.circle_cache_tf:
            self.circle_cache_tf[
                radius] = self._getTFCircleVertices(radius, points)
            self.circle_cache_ll[
                radius] = self._getLLCircleVertices(radius, points)

        ret_tf, ret_ll = [], []

        for x, y in self.circle_cache_tf[radius]:
            ret_tf.extend((x + center[0], y + center[1]))
        for x, y in self.circle_cache_ll[radius]:
            ret_ll.extend((x + center[0], y + center[1]))
        return ret_tf, ret_ll

    def DrawCircle(self, center, radius, color):
        """
        Draw an unfilled circle given center, radius and color.
        """
        unused, ll_vertices = self.getCircleVertices(
            center, radius, self.circle_segments)
        ll_count = len(ll_vertices) // 2

        v_list = self.batch.add(ll_count, gl.GL_LINES, self.group,
                                ('v2f', ll_vertices),
                                ('c4f', [color.r, color.g, color.b, 1.0] * ll_count))

        return v_list

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

        self.batch.add(ll_count, gl.GL_LINES, None,
                       ('v2f', ll_vertices),
                       ('c4f', [color.r, color.g, color.b, 1.0] * (ll_count)))

        p = Vector(center) + radius * Vector(axis)
        self.batch.add(2, gl.GL_LINES, None,
                       ('v2f', (center[0], center[1], p[0], p[1])),
                       ('c3f', [1.0, 0.0, 0.0] * 2))

    def DrawPolygon(self, vertices, color):
        """
        Draw a wireframe polygon given the world vertices (tuples) with the specified color.
        """
        if len(vertices) == 2:
            p1, p2 = vertices
            self.batch.add(2, gl.GL_LINES, None,
                           ('v2f', (p1[0], p1[1], p2[0], p2[1])),
                           ('c3f', [color.r, color.g, color.b] * 2))
        else:
            ll_count, ll_vertices = self.line_loop(vertices)

            self.batch.add(ll_count, gl.GL_LINES, None,
                           ('v2f', ll_vertices),
                           ('c4f', [color.r, color.g, color.b, 1.0] * (ll_count)))

    def DrawSolidPolygon(self, vertices, color):
        """
        Draw a filled polygon given the world vertices (tuples) with the specified color.
        """
        if len(vertices) == 2:
            p1, p2 = vertices
            self.batch.add(2, gl.GL_LINES, None,
                           ('v2f', (p1[0], p1[1], p2[0], p2[1])),
                           ('c3f', [color.r, color.g, color.b] * 2))
        else:
            tf_count, tf_vertices = self.triangle_fan(vertices)
            if tf_count == 0:
                return

            self.batch.add(tf_count, gl.GL_TRIANGLES, self.blended,
                           ('v2f', tf_vertices),
                           ('c4f', [0.5 * color.r, 0.5 * color.g, 0.5 * color.b, 0.5] * (tf_count)))

            ll_count, ll_vertices = self.line_loop(vertices)

            self.batch.add(ll_count, gl.GL_LINES, None,
                           ('v2f', ll_vertices),
                           ('c4f', [color.r, color.g, color.b, 1.0] * ll_count))

    def DrawSegment(self, p1, p2, color):
        """
        Draw the line segment from p1-p2 with the specified color.
        """
        self.batch.add(2, gl.GL_LINES, None,
                       ('v2f', (p1[0], p1[1], p2[0], p2[1])),
                       ('c3f', [color.r, color.g, color.b] * 2))

    def DrawXForm(self, xf):
        """
        Draw the transform xf on the screen
        """
        p1 = xf.position
        k_axisScale = 0.4
        p2 = p1 + k_axisScale * xf.R.x_axis
        p3 = p1 + k_axisScale * xf.R.y_axis

        self.batch.add(3, gl.GL_LINES, None,
                       ('v2f', (p1[0], p1[1], p2[0], p2[
                           1], p1[0], p1[1], p3[0], p3[1])),
                       ('c3f', [1.0, 0.0, 0.0] * 2 + [0.0, 1.0, 0.0] * 2))

    def DrawPoint(self, p, size, color):
        """
        Draw a single point at point p given a point size and color.
        """
        self.batch.add(1, gl.GL_POINTS, grPointSize(size),
                       ('v2f', (p[0], p[1])),
                       ('c3f', [color.r, color.g, color.b]))

    def DrawAABB(self, aabb, color):
        """
        Draw a wireframe around the AABB with the given color.
        """
        self.batch.add(8, gl.GL_LINES, None,
                       ('v2f', (aabb.lowerBound.x, aabb.lowerBound.y,
                                aabb.upperBound.x, aabb.lowerBound.y,
                                aabb.upperBound.x, aabb.lowerBound.y,
                                aabb.upperBound.x, aabb.upperBound.y,
                                aabb.upperBound.x, aabb.upperBound.y,
                                aabb.lowerBound.x, aabb.upperBound.y,
                                aabb.lowerBound.x, aabb.upperBound.y,
                                aabb.lowerBound.x, aabb.lowerBound.y)),
                       ('c3f', [color.r, color.g, color.b] * 8))

    def to_screen(self, point):
        """
        In here for compatibility with other frameworks.
        """
        cam = self.system.engine.current_scene.main_camera
        return cam.world_to_screen_point(Vector(point))


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

    def __init__(self, type=CLOSEST, layer=None):
        b2.b2RayCastCallback.__init__(self)
        self.collider = None
        self.colliders = []
        self.point = None
        self.normal = None
        self.hit = False
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
    def query_region(cls, bottom_left: Vector, top_right: Vector, layer: Union[int, str, None] = None,
                     type=RegionInfo.MULTIPLE) -> RegionInfo:
        """
        Query for colliders which are in a given region

        :param bottom_left: the bottom left of the region to query
        :param top_right: the bottom left of the region to query
        :param layer: the layer to filter
        :param type: type of overlap. should be one of :
            - RegionInfo.ONE => The Query Function will return only one collider found when query is finished
            - RegionInfo.MULTIPLE => The Query Function will return only all colliders found query is finished
        :return: an object of type RegionInfo, which holds information about the result of the Query
            Example of use :
                >>> PhysicsManager.query_region(
                >>>                 center=Vector(0, 0),
                >>>                 bottom_left=Vector(1, 1),
                >>>                 top_right=Vector(2, 2),
                >>>                 type=RegionInfo.ONE,
                >>>                 layer="Ground"
                >>> )
        """
        if type in (RegionInfo.MULTIPLE, RegionInfo.ONE):
            lay = None
            if layer is not None:
                lay = cls.engine.current_scene.getLayer(layer)
            cb = RegionInfo(type=type, layer=lay)

            # Make a small box.
            aabb = b2.b2AABB(lowerBound=bottom_left,
                             upperBound=top_right)

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
            cb = RayCastInfo(type=type, layer=lay)

            # normalize the direction to make it of magnitude 1
            direction = direction.normalized()

            # Calculate the destination of the ray
            dest = origin + direction * distance

            # Send the ray
            if cls.world is not None:
                cls.world.RayCast(cb, origin, (dest.x, dest.y))

            return cb
        else:
            raise ValueError(
                "RayCast Type should be one of 'RayCastInfo.MULTIPLE, RayCastInfo.CLOSEST, RayCastInfo.ANY'")

    def __init__(self, engine, **_):
        super(PhysicsManager, self).__init__(engine)

        # state
        self.debug_drawer = DebugDrawer(self)
        PhysicsManager.contact_listener = ContactListener(self)
        PhysicsManager.destruction_listener = DestructionListener(self)
        PhysicsManager.engine = self.engine

        self.vertices = list()  # type: List[pyglet.graphics.vertexdomain.VertexList]

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
                    # delete vertices
                    for vlist in self.vertices:
                        vlist.delete()
                    self.vertices.clear()

                    self._dispatch(events.DebugDraw())

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
        cls.world.renderer = self.debug_drawer

        cls.world.contactListener = self.contact_listener
        cls.world.destructionListener = self.destruction_listener

    def on_scene_stopped(self, ev: events.SceneStopped, dispatch: Callable[[Event], None]):
        PhysicsManager.world = b2.b2World(gravity=(0, -10), doSleep=True)

    def create_body(self, rb: RigidBody, e: BaseEntity):
        """
        Create the real body
        """
        try:
            body = PhysicsManager.world.CreateBody(
                b2.b2BodyDef(
                    position=e.position,
                    angle=math.radians(e.transform.angle),
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

    def __exit__(self, exc_type, exc_val, exc_tb):
        PhysicsManager.world = None

    def handle_contact(self, contact: b2.b2Contact, began: bool):
        """
        Handle a contact, it will generate collisions only
        if two colliders have made contact. And it will generate collisions enter & exit events
        only on colliders which are sensors.
        FIXME : DO NOT DESTROY ANY BODY OBJECT IN THE CALLBACK
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
        FIXME : SHOULD NOT DESTROY BODY ON COLLISION
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
                       type=OverlapInfo.ONE) -> OverlapInfo:
        return self._system_instance.overlap_circle(center, radius, layer, type)

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
    TODO
    """
    system_class = PhysicsManager
    _system_instance: PhysicsManager

    def __init__(self, instance: PhysicsManager):
        super().__init__(instance)
        self.debug = instance.debug_drawer
        self.textLine = 30

    def draw_world(self):
        """
        Draw the world
        TODO
        """

    def to_screen(self, point: Vector):
        return self._system_instance.engine.current_scene.main_camera.world_to_screen_point(point)

    def to_pixels(self, unit: float):
        return self._system_instance.engine.current_scene.main_camera.unit_to_pixels(unit)

    def getColor(self, color: Sequence[int]):
        return b2.b2Color([c / 255 for c in color[:3]])

    def draw_circle(self, center: Vector, radius: float, color: Tuple[int, int, int, int]):
        vlist = self.debug.DrawCircle(self.to_screen(center), self.to_pixels(radius), self.getColor(color))
        self._system_instance.vertices.append(vlist)

    def DrawStringAt(self, point: Vector, str, color=(229, 153, 153, 255)):
        """
        Draw some text, str, at screen coordinates (x, y).
        """
        win = kge.ServiceProvider.getWindow()

        point = self.to_screen(point)

        label = pyglet.text.Label(str,
                          font_size=15, x=point.x, y=point.y,
                          color=color, batch=win.batch, group=win.render_layers[-1])

        self._system_instance.vertices.append(label)

    def Print(self, str, color=(229, 153, 153, 255)):
        """
        Draw some text, str, at screen coordinates (x, y).
        """
        win = kge.ServiceProvider.getWindow()
        label = pyglet.text.Label(str,
                          font_size=15, x=5, y=win.window.height -
                                               self.textLine, color=color, batch=win.batch,
                          group=win.render_layers[-1])

        self._system_instance.vertices.append(label)
        self.textLine += 15


if __name__ == '__main__':
    with PhysicsManager(None) as p_m:
        pass
