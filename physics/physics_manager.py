import time
from collections import deque
from typing import Callable, Union, Deque, Optional

import math

import kge
from kge.utils.vector import Vector
from kge.physics.colliders import Collider
from kge.physics.rigid_body import RigidBody
from kge.core import events
from kge.core.constants import FIXED_DELTA_TIME
from kge.core.events import Event
from kge.core.service import Service
from kge.core.system import System
import Box2D as b2

from kge.physics.events import CollisionEnter, CollisionExit, CreateBody, BodyCreated, BodyDestroyed, DestroyBody, PhysicsUpdate


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
    NOTE : TO TEST
    """
    MULTIPLE = 1
    ONE = 0

    def __init__(self, type=ONE, layer=None):
        super().__init__()
        self.type = type
        self.colliders = []
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


class PhysicsManager(System):
    """
    The system that handles movements, collision detection and can perform overlaps for region query and ray casts
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
                       type=OverlapInfo.ONE) -> OverlapInfo:
        """
        TODO : Add a notice here because it is much for 'overlaping Squares' than circles
        Query for colliders which are in a given circle region


        :param origin: The center point of the circle to overlap
        :param radius: the radius of the circle to overlap
        :param layer: the layer to filter
        :param type: type of overlap. should be one of :
            - OverlapInfo.ONE => The Overlap Function will return only one collider found when overlapping
            - OverlapInfo.MULTIPLE => T The Overlap Function will return only all colliders found when overlapping
        :return: an object of type OverlapInfo, which holds information about the result of the Overlap
            Example of use :
                >>> PhysicsManager.overlap_circle( center=Vector(0, 0), radius=1, type=OverlapInfo.ONE, layer="Ground" )
        """
        if type in (OverlapInfo.MULTIPLE, OverlapInfo.ONE):
            lay = None
            if layer is not None:
                lay = cls.engine.current_scene.getLayer(layer)
            cb = OverlapInfo(type=type, layer=lay)

            # Make a small box.
            aabb = b2.b2AABB(lowerBound=center - Vector(radius, radius),
                             upperBound=center + Vector(radius, radius))

            # Query the world for overlapping shapes.
            cls.world.QueryAABB(cb, aabb)

            return cb
        else:
            raise ValueError(
                "Overlap Type should be one of 'OverlapInfo.ONE or OverlapInfo.MULTIPLE'")

    @classmethod
    def ray_cast(cls, origin: Vector, direction: Vector, distance: float, layer: Union[int, str, None] = None,
                 type=RayCastInfo.CLOSEST, ) -> RayCastInfo:
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
            cls.world.RayCast(cb, origin, (dest.x, dest.y))

            return cb
        else:
            raise ValueError(
                "RayCast Type should be one of 'RayCastInfo.MULTIPLE, RayCastInfo.CLOSEST, RayCastInfo.ANY'")

    def __init__(self, engine):
        super(PhysicsManager, self).__init__(engine)

        # state
        PhysicsManager.contact_listener = ContactListener(self)
        PhysicsManager.destruction_listener = DestructionListener(self)
        PhysicsManager.engine = self.engine
        # type: Union[Callable[[Event], None], None]
        self._dispatch = self.engine.dispatch
        self.accumulated_time = 0
        self.last_tick = None
        self.start_time = None
        self.time_step = FIXED_DELTA_TIME

        # TODO : Implement layers in order to ignore collisions within different layers
        self.layers_to_ignore = {}

    def on_physics_update(self, idle_event: PhysicsUpdate, dispatch: Callable[[Event], None]):
        """
        FIXME : SHOULD HAPPEN IN PhysicsUpdate Event
        """
        if not self.pause:
            if PhysicsManager.world:
                # Only a fixed number of frames per second
                if self.last_tick is None:
                    self.last_tick = time.monotonic()
                this_tick = time.monotonic()
                self.accumulated_time += this_tick - self.last_tick
                self.last_tick = this_tick

                # self.logger.info(self.accumulated_time)

                while self.accumulated_time >= self.time_step:
                    PhysicsManager.world.Step(
                        FIXED_DELTA_TIME * idle_event.time_scale, 10, 10)
                    PhysicsManager.world.ClearForces()

                    # send fixed update call
                    # self._dispatch(FixedUpdate(
                    #     fixed_delta_time=FIXED_DELTA_TIME * idle_event.time_scale
                    # ), immediate=True)
                    self.accumulated_time += -self.time_step

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
        PhysicsManager.world = b2.b2World(gravity=(0, -10), doSleep=True)
        PhysicsManager.world.contactListener = self.contact_listener
        PhysicsManager.world.destructionListener = self.destruction_listener

    def on_scene_stopped(self, ev: events.SceneStopped, dispatch: Callable[[Event], None]):
        PhysicsManager.world = b2.b2World(gravity=(0, -10), doSleep=True)

    def on_create_body(self, ev: CreateBody, dispatch: Callable[[Event], None]):
        """
        Create a body
        """
        rb = ev.body_component
        e = ev.entity

        if rb.is_ghost:
            manager = kge.ServiceProvider.getEntityManager()
            manager.add_component(e, rb, "_body")
            # ev.entity.addComponent("_body", rb)

        body = PhysicsManager.world.CreateBody(
            b2.b2BodyDef(
                position=e.position,
                angle=math.radians(e.transform.angle),
                type=rb.body_type,
                active=rb.active,
                allowSleep=True,
                awake=True,
                fixedRotation=rb.fixed_rotation,
                userData=rb,
                gravityScale=rb.gravity_scale,
                bullet=True,
            )
        )  # type: b2.b2Body

        # Set mass, velocity and inertia of the body
        body.mass = rb.mass
        body.linearVelocity = rb.velocity
        body.angularVelocity = rb.angular_velocity
        body.inertia = rb.inertia

        # the body has been created
        event = BodyCreated(
            entity=ev.entity,
            body=body
        )
        event.onlyEntity = ev.entity
        dispatch(event)

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

        self.logger.debug(
            f"Contact {'began' if began else 'ended'} ! with, '{collider_a}'  and '{collider_b}'")

        if isinstance(collider_a, Collider) and isinstance(collider_b, Collider):
            # Deactivate contact if one of the colliders is not active
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
            PhysicsManager.world.DestroyBody(ev.body_component.body)
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
        self.logger.debug(f"GoodBye... {fixture.userData}")

    def pre_solve(self, contact: b2.b2Contact):
        """
        Pre Solve a contact in order to deactivate contact
        """
        collider_a = contact.fixtureA.userData
        collider_b = contact.fixtureB.userData

        if isinstance(collider_a, Collider) and isinstance(collider_b, Collider):
            # disable contact if one of the colliders is not active
            if not collider_a.active or not collider_b.active:
                contact.enabled = False
        else:
            contact.enabled = False


class Physics(Service):
    system_class = PhysicsManager
    _system_instance: PhysicsManager

    def ray_cast(self, origin: Vector, direction: Vector, distance: float, layer: Union[int, str, None] = None,
                 type=RayCastInfo.CLOSEST) -> RayCastInfo:
        return self._system_instance.ray_cast(origin, direction, distance, layer, type)

    def overlap_circle(self, center: Vector, radius: float, layer: Union[int, str, None] = None,
                       type=OverlapInfo.ONE) -> OverlapInfo:
        return self._system_instance.overlap_circle(center, radius, layer, type)


if __name__ == '__main__':
    with PhysicsManager(None) as p_m:
        pass
