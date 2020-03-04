import time
from collections import deque
from itertools import chain
from typing import Callable, Union, Deque, Optional, List, Tuple

import math

import pyglet

import kge
from kge.core.component_system import ComponentSystem
from kge.core.entity import BaseEntity
from kge.utils.vector import Vector
from kge.physics.colliders import Collider
from kge.physics.rigid_body import RigidBody, RigidBodyType
from kge.core import events
from kge.core.constants import FIXED_DELTA_TIME
from kge.core.events import Event
from kge.core.service import Service
# from kge.core.system import System
import Box2D as b2

from kge.physics.events import CollisionEnter, CollisionExit, CreateBody, BodyCreated, BodyDestroyed, DestroyBody, \
    PhysicsUpdate, CollisionBegin, CollisionEnd


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


class PhysicsManager(ComponentSystem):
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
            if cls.world is not None:
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
        self.time_step = FIXED_DELTA_TIME

        # only rigid bodies and colliders supported
        self.components_supported = [RigidBody, Collider]

        # bodies to destroy
        self.garbage_bodies = [] # type: List[b2.b2Body]
        # bodies to create
        self.new_bodies = [] # type: List[Tuple[RigidBody, BaseEntity]]

        # TODO : Implement layers in order to ignore collisions within different layers
        self.layers_to_ignore = {}

    def on_physics_update(self, event: PhysicsUpdate, dispatch: Callable[[Event], None]):
        """
        Update physics
        """
        if not self.pause:
            if PhysicsManager.world:
                try:
                    # Destroy garbage bodies
                    # FIXME : If bugging verifiy
                    for body in self.garbage_bodies:
                        body.active = False
                    self.garbage_bodies.clear()

                    # Create new bodies
                    for rb, e in self.new_bodies:
                        self.create_body(rb, e)
                    self.new_bodies.clear()

                    PhysicsManager.world.Step(
                        FIXED_DELTA_TIME * event.time_scale, 10, 10)
                    PhysicsManager.world.ClearForces()

                    # Launch Physics Update on rigid bodies
                    rigid_bodies = self.active_components()  #filter(lambda c: isinstance(c, RigidBody) and c.body_type != RigidBodyType.STATIC,self.active_components())
                    # rigid_bodies = filter(lambda c: isinstance(c, RigidBody) and c.body_type != RigidBodyType.STATIC,self.active_components())
                    for rb in rigid_bodies:  # type: RigidBody
                        rb.__fire_event__(event, dispatch)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(e)

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
        PhysicsManager.world = b2.b2World(gravity=(0, -10), doSleep=True)
        PhysicsManager.world.contactListener = self.contact_listener
        PhysicsManager.world.destructionListener = self.destruction_listener

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
        FIXME : SHOULD NOT HAPPEN WHEN WORLD IS STEPPING
        """
        rb = ev.body_component
        e = ev.entity

        if rb.is_ghost:
            manager = kge.ServiceProvider.getEntityManager()
            manager.add_component(e, rb, "_body")
            # ev.entity.addComponent("_body", rb)c

        # rb.entity = ev.entity
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

            # try:
            # self.logger.debug(f"Destroying {ev.body_component} of {ev.entity}")
            ev.body_component.is_active = False
            colliders = ev.entity.getComponents(kind=Collider)
            for col in colliders:
                col.is_active = False
            # FIXME : SHOULD DESTROY LATER
            self.garbage_bodies.append(ev.body_component.body)
            # set user data to none in order to free it
            ev.body_component.body.userData = None
            # pyglet.clock.schedule_once(lambda dt: PhysicsManager.world.DestroyBody(ev.body_component.body), 1)
            # ev.body_component.body.active = False
            # PhysicsManager.world.DestroyBody(ev.body_component.body)
            # except Exception as e:
            #     import traceback
            #     traceback.print_exc()
            #     print(e)
            # else:
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


if __name__ == '__main__':
    with PhysicsManager(None) as p_m:
        pass
