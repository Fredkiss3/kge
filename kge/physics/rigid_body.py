# import Box2D as b2
# import Box2D as b2
import platform
import sys
from enum import Enum, auto
from typing import Tuple, Union, Callable, Optional

if sys.platform == "win32":
    if platform.architecture()[0] == "64bit":
        import kge.extra.win64.Box2D as b2
        from kge.extra.win64.Box2D import (
            b2_dynamicBody,
            b2_kinematicBody,
            b2_staticBody,
        )
    elif platform.architecture()[0] == "32bit":
        import kge.extra.win32.Box2D as b2
        from kge.extra.win32.Box2D import (
            b2_dynamicBody,
            b2_kinematicBody,
            b2_staticBody,
        )
elif sys.platform == 'darwin':
    if platform.architecture()[0] == "64bit":
        import kge.extra.darwin_arm64.Box2D as b2
        from kge.extra.darwin_arm64.Box2D import (
            b2_dynamicBody,
            b2_kinematicBody,
            b2_staticBody,
        )
else:
    import kge.extra.linux64.Box2D as b2
    from kge.extra.linux64.Box2D import (
        b2_dynamicBody,
        b2_kinematicBody,
        b2_staticBody,
    )

import math

import pyglet
# from Box2D import (
#     b2_dynamicBody,
#     b2_kinematicBody,
#     b2_staticBody,
# )

import kge
from kge.core.constants import FIXED_DELTA_TIME
from kge.utils.vector import Vector
from kge.core.component import BaseComponent

from kge.core.entity import BaseEntity
from kge.core import events
from kge.core.events import Event, DestroyBody, BodyCreated, CreateBody


class RigidBodyType(Enum):
    STATIC = auto()
    DYNAMIC = auto()
    KINEMATIC = auto()


class RigidBody(BaseComponent):
    """
    A component that manages all physics of the entity.
    In practice it just an interface that holds and modify information about the real body.
    An entity should only have one of this in its components.
    You should also note that when adding a RigidBody to an entity, the positions controls are switched to
    the component, so if you want to later get the control of the position, you should use
    the component directly
    """
    # Body Types

    _body_types = {
        RigidBodyType.STATIC: b2_staticBody,
        RigidBodyType.DYNAMIC: b2_dynamicBody,
        RigidBodyType.KINEMATIC: b2_kinematicBody,
    }

    def __init__(self, body_type: RigidBodyType = RigidBodyType.DYNAMIC):
        """
        Initialize the rigid body
        :param body_type: the Body type. It should be one of : 'RigidBody.STATIC', 'RigidBody.DYNAMIC',
        'RigidBody.KINEMATIC'.
        """
        super().__init__(None)

        # set the entity
        self._entity = None  # type: Union[BaseEntity, None]

        # states
        if body_type in [RigidBodyType.STATIC, RigidBodyType.DYNAMIC, RigidBodyType.KINEMATIC]:
            self._body_type = self._body_types[body_type]
            self.type = body_type
        else:
            raise ValueError(
                "Body type must be one of 'RigidBodyType.STATIC', 'RigidBodyType.DYNAMIC', 'RigidBodyType.KINEMATIC' ")

        # private attributes
        self._body = None  # type: Union[b2.b2Body, None]
        self._mass = 1
        self._velocity = Vector(0, 0)
        self._angular_velocity = 0
        self._active = True
        self._gravity_scale = 1
        self._inertia = 0
        self._fixed_rotation = False
        self._sleeping = False
        self._angle = 0
        self._position = Vector.Zero()
        self._drag = 0
        self._angular_drag = 0

        try:
            self._physics_system = kge.Physics
        except:
            self._physics_system = None

        # Vertices for the transform
        self._tranform_vlist = None  # type: Optional[pyglet.graphics.vertexdomain.VertexList]

        # public
        self.is_ghost = False

    @property
    def vlist(self):
        return self._tranform_vlist

    @vlist.setter
    def vlist(self, value):
        if isinstance(value, pyglet.graphics.vertexdomain.VertexList) or value is None:
            self._tranform_vlist = value
        else:
            raise TypeError("Vertices should be of type 'pyglet.graphics.vertexdomain.VertexList'")

    @property
    def fixed_rotation(self):
        return self._fixed_rotation

    @fixed_rotation.setter
    def fixed_rotation(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("Fixed rotation attribute should be a bool")
        elif self.type != RigidBodyType.DYNAMIC:
            raise AttributeError("Fixed rotation attribute is only available on Dynamic rigid bodies")

        self._fixed_rotation = val

        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.fixedRotation = val
            pass

    @property
    def entity(self) -> BaseEntity:
        return self._entity

    @entity.setter
    def entity(self, e: BaseEntity):
        if isinstance(e, BaseEntity):
            if e.getComponent(kind=RigidBody) is not None:
                raise AttributeError(f"There is already another RigidBody component attached to '{e}'")

            # set entity
            self._entity = e

    @property
    def velocity(self) -> Vector:
        if self._body is not None and self._physics_system.world is not None:
            self._velocity = Vector(self._body.linearVelocity.x, self._body.linearVelocity.y)
        return Vector(self._velocity)

    @velocity.setter
    def velocity(self, val: Vector):
        if not isinstance(val, Vector):
            raise TypeError("Velocity should be a vector")

        self._velocity = val

        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.linearVelocity = (*val,)

    @property
    def mass(self) -> float:
        if self._body is not None and self._physics_system.world is not None:
            self._mass = self._body.mass
        return self._mass

    @mass.setter
    def mass(self, val: float):
        if not isinstance(val, (float, int)):
            raise TypeError("Mass should be either a float or an int")

        self._mass = val

        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.mass = val
            pass

    @property
    def active(self) -> bool:
        if self._body is not None and self._physics_system.world is not None:
            self._active = self._body.active
        return self._active

    @active.setter
    def active(self, val: bool):
        if not isinstance(val, (float, int)):
            raise TypeError("Mass should be either a float or an int")

        self._active = val

        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.active = val
            pass

    @property
    def gravity_scale(self):
        if self._body is not None and self._physics_system.world is not None:
            self._gravity_scale = self._body.gravityScale
        return self._gravity_scale

    @gravity_scale.setter
    def gravity_scale(self, scale: float):
        if not isinstance(scale, (float, int)):
            raise TypeError("Scale should be a number")

        self._gravity_scale = scale

        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.gravityScale = scale
            pass

    @property
    def inertia(self):
        if self._body is not None and self._physics_system.world is not None:
            self._inertia = self._body.inertia
        return self._inertia

    @inertia.setter
    def inertia(self, val: float):
        if not isinstance(val, (float, int)):
            raise TypeError("Inertia should be a number")

        self._inertia = val

        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.inertia = val
            pass

    @property
    def angular_velocity(self):
        if self._body is not None and self._physics_system.world is not None:
            self._angular_velocity = self._body.angularVelocity
        return self._angular_velocity

    @angular_velocity.setter
    def angular_velocity(self, val: float):
        if not isinstance(val, (float, int)):
            raise TypeError("Angular velocity should be a number")

        self._angular_velocity = val
        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.angularVelocity = val
            pass

    @property
    def b_type(self):
        return self._body_type

    @property
    def body_type(self):
        if self.b_type == b2_dynamicBody:
            return RigidBodyType.DYNAMIC
        elif self.b_type == b2_kinematicBody:
            return RigidBodyType.KINEMATIC
        else:
            return RigidBodyType.STATIC

    @property
    def body(self) -> b2.b2Body:
        return self._body

    @property
    def awake(self):
        """
        Set the body to awake
        """
        if self._body is not None and self._physics_system.world is not None:
            self._sleeping = self._body.awake

        return self._sleeping

    @awake.setter
    def awake(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("awake should be a bool")

        self._sleeping = val
        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.awake = val
            pass

    @property
    def angle(self):
        """
        Get angle in degrees
        """
        if self._body is not None and self._physics_system.world is not None:
            self._angle = math.degrees(self._body.angle)
        return self._angle

    @angle.setter
    def angle(self, val: float):
        """
        set angle in degrees
        """
        if not isinstance(val, (float, int)):
            raise TypeError("angle should be a number")

        self._angle = val
        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.angle = math.radians(val)

    @property
    def position(self):
        if self._body is not None and self._physics_system.world is not None:
            self._position = Vector(self._body.position.x, self._body.position.y)
        return self._position

    @position.setter
    def position(self, val: Union[Vector, tuple]):
        if not isinstance(val, (Vector, tuple)):
            raise TypeError("Position should be either a tuple of Numbers or a vector")

        # set vector
        val = Vector(val)

        self._position = val
        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.position = (val.x, val.y)

    @property
    def drag(self):
        """
        The
        """
        return self._drag

    @drag.setter
    def drag(self, val: float):
        if not isinstance(val, (float, int)):
            raise TypeError("Drag should be a float !")

        self._drag = val
        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.linearDamping = val

    @property
    def angular_drag(self):
        """
        The resistance to the rotation
        """
        return self._angular_drag

    @angular_drag.setter
    def angular_drag(self, val: float):
        if not isinstance(val, (float, int)):
            raise TypeError("Angular Drag should be a float !")

        self._angular_drag = val
        if self._body is not None and self._physics_system.world is not None:
            while self._physics_system.world.locked:
                continue
            self._body.angularDamping = val

    def on_body_created(self, ev: BodyCreated, dispatch: Callable[[Event], None]):
        """
        if the real body has been created then
        attach it to this
        """
        if ev.entity == self.entity:
            # set the real body
            self._body = ev.rb.body

    def on_body_destroyed(self, ev, _):
        if ev.entity == self.entity:
            self._body = None
            manager = kge.ServiceProvider.getEntityManager()
            manager.remove_component(self.entity, kind=RigidBody)

            # Delete vertices if there has been created
            if self._tranform_vlist is not None:
                self._tranform_vlist.delete()

    def on_init(self, ev: events.Init, dispatch: Callable[[Event], None]):
        """
        At initialization we must create the body
        """
        if not self.is_ghost:
            # look if there is a body created by a collider of the entity
            ghost_body = self.entity.getComponent(kind=RigidBody)

            if ghost_body is not None:
                if ghost_body.is_ghost:
                    # delete the real body in the world
                    ev_ = DestroyBody(
                        entity=self.entity,
                        rb=ghost_body
                    )
                    ev_.onlyEntity = self.entity
                    dispatch(ev_)

            ev_ = CreateBody(
                entity=self.entity,
                rb=self
            )

            # create the real body
            ev_.onlyEntity = self.entity
            dispatch(ev_)

    def add_force(self, force: Vector, impulse: bool = False, point: Vector = Vector.Zero()):
        """
        add a force to the rigid body.
        You can specify a point in the body to add the force.
        The point should be a relative point to the center of the rigid body.
        """
        if self._body is None:
            raise AttributeError("Body has not been created yet !")

        if not (isinstance(force, Vector) and isinstance(impulse, bool) and isinstance(point, Vector)):
            raise TypeError("Force and point should be vectors and impulse should be a bool")

        point = self._body.GetWorldPoint(localPoint=(point.x, point.y))
        force = self._body.GetWorldVector(localVector=(force.x, force.y))

        while self._physics_system.world.locked:
            continue
        if not impulse:
            self._body.ApplyForce(force, point, True)
        else:
            self._body.ApplyLinearImpulse(force, point, True)

    def add_torque(self, torque: float, impulse: bool = False):
        """
        add a rotation torque to the rigid body
        """
        if self._body is None:
            raise AttributeError("Body has not been created yet !")

        if not (isinstance(torque, float) and isinstance(impulse, bool)):
            raise TypeError("torque should be a number and impulse should be a bool")

        if not impulse:
            self._body.ApplyTorque(torque, True)
        else:
            self._body.ApplyAngularImpulse(torque, True)

    def __repr__(self):
        return f"component {type(self).__name__} ({self.type}) of entity '{self.entity}'"

    def move_position(self, destination: Union[Vector, Tuple[float, float]]):
        """
        move towards a destination. This methods is collision safe.
        Moves the rigid body to the specified position by calculating the appropriate
        linear velocity required to move  the rigid body to that position
        during the next physics update.

        Warning : Do not use this method to move between large distances

        :param destination: destination
        :return:
        """
        vel = (destination - self.entity.position) / FIXED_DELTA_TIME
        self.velocity = Vector(*vel)

    def move_rotation(self, angle: float):
        """
        Rotate towards an angle. This methods is collision safe.
        Rotate the rigid body to the specified angle by calculating the appropriate
        angular velocity required to rotate the rigid body to that position
        during the next physics update.

        Warning : Do not use this method to rotate between large angles

        :param angle: angle of destination
        :return:
        """
        vel = (angle - self.entity.angle) / FIXED_DELTA_TIME
        self.angular_velocity = vel

    @body.setter
    def body(self, value: b2.b2Body):
        if not isinstance(value, b2.b2Body):
            raise TypeError("Body should be of type (Box2D.b2Body)")
        if self._body is not None:
            raise AttributeError("Can only set Body Property once")

        self._body = value


if __name__ == '__main__':
    class Player(BaseEntity):
        pass


    # help(RigidBody)
    #
    p = Player()
    rb = RigidBody(body_type=RigidBodyType.DYNAMIC)
    print(rb.entity)
    p.addComponent(rb)
    print(rb.entity)
    print(p.components)
    # rb.velocity = (5, 5)
    # print(RigidBody.DYNAMIC, type(RigidBody.DYNAMIC, ))
