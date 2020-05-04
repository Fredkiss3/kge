# import Box2D as b2
# import Box2D as b2
import platform
import sys
from typing import Union, Callable, List, Optional

import pyglet

import kge
from kge.core import events
from kge.core.component import BaseComponent
from kge.core.entity import BaseEntity
from kge.physics.rigid_body import RigidBody, RigidBodyType
from kge.utils.vector import Vector

if sys.platform == "win32":
    if platform.architecture()[0] == "64bit":
        import kge.extra.win64.Box2D as b2
    elif platform.architecture()[0] == "32bit":
        import kge.extra.win32.Box2D as b2
else:
    import kge.extra.linux64.Box2D as b2

from kge.core.events import Event, BodyCreated, BodyDestroyed, CreateBody


class Collider(BaseComponent):
    """
    The only component that handles collisions
    """

    def __init__(self,
                 sensor: bool = False,
                 offset: Vector = Vector.Zero(),
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1,
                 ):
        super().__init__(None)
        if not isinstance(sensor, bool):
            raise TypeError("Sensor should be a bool")

        # does this collider pass through objects ?
        self.isSensor = sensor

        # the real fixture
        self._fixture = None  # type: Union[b2.b2Fixture, None]
        self._rb = None  # type: Union[RigidBody, None]

        if not isinstance(offset, Vector):
            raise TypeError("Offset should be a vector")

        # the position of the collider relative to the parent body
        self._offset = offset
        self._density = density
        self._bounciness = bounciness
        self._friction = friction

        # Vertices of the shape of the collider
        self._shape_vlist = None  # type: Optional[pyglet.graphics.vertexdomain.VertexList]

    @property
    def fixture(self):
        return self._fixture

    @property
    def vlist(self):
        return self._shape_vlist

    @vlist.setter
    def vlist(self, value):
        if isinstance(value, pyglet.graphics.vertexdomain.VertexList) or value is None:
            self._shape_vlist = value
        else:
            raise TypeError(
                "Vertices should be of type 'pyglet.graphics.vertexdomain.VertexList'")

    @property
    def rb_attached(self):
        """
        Get the RigidBody attached to the collider
        """
        return self._rb

    @property
    def offset(self):
        return Vector(self._offset)

    @property
    def shape(self) -> b2.b2Shape:
        raise NotImplementedError(
            "Do not use Collider class, instead use subclasses of collider like BoxCollider or CircleCollider")

    @property
    def friction(self):
        return self._friction

    @friction.setter
    def friction(self, val: float):
        if not isinstance(val, (float, int)):
            raise TypeError("friction should be a number")

        self._friction = val

        if self._fixture is not None:
            self._fixture.friction = val

    @property
    def bounciness(self):
        return self._bounciness

    @bounciness.setter
    def bounciness(self, val: float):
        if not isinstance(val, (float, int)):
            raise TypeError("bounciness should be a number")

        self._bounciness = val

        if self._fixture is not None:
            self._fixture.restitution = val

    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, val: float):
        if not isinstance(val, (float, int)):
            raise TypeError("density should be a number")

        self._density = val

        if self._fixture is not None:
            self._fixture.density = val

    def __recreate(self):
        self._rb.body.CreateFixture(b2.b2FixtureDef(
            density=self.density,
            restitution=self.bounciness,
            isSensor=self.isSensor,
            shape=self.shape,
            friction=self.friction,
            userData=self
        ))

        self._fixture = self._rb.body.fixtures[-1]  # type: b2.b2Fixture

    def __destroy(self):
        self._rb.body.DestroyFixture(self._fixture)

    def __create(self, body=None):
        """
        Create the fixture
        """
        if body is None:
            body = self._rb.body

        physics = kge.ServiceProvider.getPhysics()

        while physics.world.locked:
            continue

        body.CreateFixture(
            defn=b2.b2FixtureDef(
                density=self.density,
                restitution=self.bounciness,
                isSensor=self.isSensor,
                shape=self.shape,
                friction=self.friction,
                userData=self
            )
        )

        # our fixture is the last
        self._fixture = body.fixtures[-1]  # type: b2.b2Fixture

    ############################
    #         Events           #
    ############################

    def on_body_created(self, ev: BodyCreated, _):
        if ev.entity == self.entity:
            rb = self.entity.getComponent(kind=RigidBody)  # type: RigidBody
            if rb is not None:
                self._rb = rb

            # create a fixture for this body
            if self._fixture is None:
                self.__create(body=ev.rb.body)

    def on_body_destroyed(self, ev: BodyDestroyed, _):
        if ev.entity == self.entity:
            manager = kge.ServiceProvider.getEntityManager()
            manager.remove_component(self.entity, kind=Collider)

            # Delete vertices if there has been created
            if self._shape_vlist is not None:
                self._shape_vlist.delete()

    def on_init(self, ev: events.Init, dispatch: Callable[[Event], None]):
        """
        on initialisation
        """
        rb = self.entity.getComponent(kind=RigidBody)  # type: RigidBody

        if rb is not None:
            # create a fixture for this
            self._rb = rb

            if rb.body is not None:
                # our fixture is the last fixture
                self.__create()
        else:
            # create a ghost rigid body
            rb = RigidBody(body_type=RigidBodyType.STATIC)
            rb.is_ghost = True
            event = CreateBody(
                entity=self.entity,
                rb=rb
            )

            event.onlyEntity = self.entity
            dispatch(event)


class BoxCollider(Collider):
    """
    A component that handles collision in a box shape
    """

    def __init__(self,
                 box: Vector = None,
                 sensor: bool = False,
                 offset: Vector = Vector.Zero(),
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1, ):
        """
        initialize the collider

        :param box: a vector which describes the box of the collider in form of Vector(width, height)
                    default is set to entity size
        :param offset: The position of the collider relative to the parent body
        """
        super().__init__(sensor, offset, bounciness, friction, density)

        if box is not None and not isinstance(box, Vector):
            raise TypeError("Box should be a vector")

        # the box
        self._box = box

    @property
    def box(self):
        return Vector(self._box)

    def on_init(self, ev: events.Init, dispatch: Callable[[Event], None]):
        # if box is not set then scale it to the entity scale
        if self._box is None:
            box = self.entity.transform.scale
        else:
            box = self._box

        self._box = abs(Vector(box.x / 2, box.y / 2))
        super(BoxCollider, self).on_init(ev, dispatch)

    @property
    def shape(self) -> b2.b2Shape:
        return b2.b2PolygonShape(box=(
            *self._box, (*self._offset,), 0
        ))

    def setBox(self, box: Vector):
        """
        Change the 'Box' Value of the Collider
        """
        if not isinstance(box, Vector):
            raise TypeError("Box Property should be a vector")

        if self._fixture is not None:
            while kge.Physics.world.locked:
                continue

            self._box = box
            self._fixture.shape.box = *self._box,


class CameraCollider(BoxCollider):
    """
    # NOTE : IS THIS THE BEST WAY ?
    A Box collider attached to the camera
    """

    def __init__(self, box: Vector = None):
        super().__init__(box, sensor=True, offset=Vector.Zero(), bounciness=0, friction=0, density=1)
        # set the entity
        self._entity = None  # type: Union[kge.Camera, None]

    @property
    def entity(self) -> "kge.Camera":
        return self._entity

    @entity.setter
    def entity(self, e: "kge.Camera"):
        if e is not None and not isinstance(e, kge.Camera):
            raise TypeError(f"Camera Collider can only be attached to a camera")

        # set entity
        self._entity = e


class PassThroughCollider(BoxCollider):
    """
    A component that handles collision in a box shape but allow passing through in certain directions
    """

    def __init__(self,
                 pass_up: bool = False,
                 pass_down: bool = False,
                 pass_left: bool = False,
                 pass_right: bool = False,
                 box: Vector = None,
                 sensor: bool = False,
                 offset: Vector = Vector.Zero(),
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1,
                 ):
        """
        initialize the collider

        :param box: a vector which describes the box of the collider in form of Vector(width, height)
        :param offset: The position of the collider relative to the parent body
        """
        super().__init__(box, sensor, offset, bounciness, friction, density)

        # Pass directions
        self.pass_up = pass_up
        self.pass_down = pass_down
        self.pass_left = pass_left
        self.pass_right = pass_right


class CircleCollider(Collider):
    """
    A component that handles collision in a circle shape
    """

    def __init__(self,
                 radius: float = None,
                 center: Vector = Vector.Zero(),
                 sensor: bool = False,
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1.0,
                 ):
        """
        initialize the collider

        :param radius: the radius of the collider
        :param center: The position of the center of the collider relative to the parent body
        """
        super().__init__(sensor, center, bounciness, friction, density)

        if radius is not None and not isinstance(radius, (float, int)):
            raise TypeError("Radius should be a number")

        # the box
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    def on_init(self, ev: events.Init, dispatch: Callable[[Event], None]):
        # if no radius has been provided, then set it to the max scale of the entity
        if self._radius is None:
            self._radius = max(self.entity.transform.scale.x,
                               self.entity.transform.scale.y) / 2

        super(CircleCollider, self).on_init(ev, dispatch)

    @property
    def shape(self) -> b2.b2CircleShape:
        return b2.b2CircleShape(
            pos=(*self._offset,), radius=self._radius
        )


class CapsuleCollider(Collider):
    """
    A capsule collider is a combination of three colliders :
        One BoxCollider at the center
        Two CircleColliders at the edges
    TODO
    """
    pass


class PolygonCollider(Collider):
    """
    A component that handles collision within in a polygon shape
    """

    def __init__(self,
                 vertices: List[Vector],
                 sensor: bool = False,
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1,
                 ):
        """
        initialize the collider

        :param vertices: a list of points of the collider in this form :
            vertices=[Vector(-1, -1), Vector(2, 2), Vector(1, 1)].
            each point is relative to the parent body
        """
        super().__init__(sensor, Vector.Zero(), bounciness, friction, density)

        if len(vertices) < 3:
            raise ValueError(
                "Polligon collider should have 3 or more vertices")

        # the vertices
        self._vertices = vertices

    @property
    def shape(self) -> b2.b2PolygonShape:
        return b2.b2PolygonShape(
            vertices=[(*v,) for v in self._vertices]
        )


class TriangleCollider(Collider):
    """
    A component that handles collisions in a triangle shape
    """

    def __init__(self, vertices: List[Vector] = None, center: Vector = Vector.Zero(), sensor: bool = False,
                 bounciness: float = 0,
                 friction: float = 0, density: float = 1.0):
        """
        initialize the collider

        :param center: The position of the center of the collider relative to the parent body
        :param vertices: The vertices of the collider relative to the parent body
        """
        super().__init__(sensor, center, bounciness, friction, density)

        if vertices is not None and len(vertices) < 3:
            raise ValueError("Triangle Collider accepts three vertices")
        elif vertices is not None:
            self._vertices = vertices[:3]

        self._vertices = vertices

    def on_init(self, ev: events.Init, dispatch: Callable[[Event], None]):
        if self._vertices is None:
            self._vertices = []
            vertices = [
                Vector(0, 1 / 2),
                Vector(1 / 2, -1 / 2),
                Vector(-1 / 2, -1 / 2),
            ]

            # vertices.reverse()

            for v in vertices:
                self._vertices.append(
                    (Vector(v.x * self.entity.transform.scale.x,
                            v.y * self.entity.transform.scale.y))
                )
            super(TriangleCollider, self).on_init(ev, dispatch)

    @property
    def shape(self) -> b2.b2PolygonShape:
        return b2.b2PolygonShape(
            vertices=[(v.x, v.y) for v in self._vertices]
        )


class LineCollider(Collider):
    """
    A component that handles collisions which occurs in a line segment shape
    """

    def __init__(self,
                 point1: Vector,
                 point2: Vector,
                 sensor: bool = False,
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1,
                 ):
        """
        initialize the collider

        :param point1: The origin point relative to the parent
        :param point2: The destination point relative to the parent
            # each point is relative to the parent body
            >>> collider = LineCollider(
            >>>         point1=Vector(-1, -1),
            >>>         point2=Vector(1, 1)
            >>> )
        """
        super().__init__(sensor, Vector.Zero(), bounciness, friction, density)

        # the vertices
        self._vertices = [point1, point2]

    @property
    def shape(self) -> b2.b2EdgeShape:
        return b2.b2EdgeShape(
            vertices=[(*v,) for v in self._vertices]
        )


class EdgeCollider(Collider):
    """
    A component that handles collisions which occurs in a sequence of line segments that forms a circular list.
    """

    def __init__(self,
                 vertices: List[Vector],
                 sensor: bool = False,
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1,
                 ):
        """
        initialize the collider. When you give vertices, the collider automatically closes itself with the
        last vertex and first vertex forming a segment. This collider accept inside and outside collisions

        :param vertices: a list of points of the collider in this form :
            # each point is relative to the parent body
            >>> collider = LineCollider(
            >>> vertices=[
            >>>   Vector(-1, -1), Vector(2, 2), Vector(1, 1)
            >>> ])
        """
        super().__init__(sensor, Vector.Zero(), bounciness, friction, density)

        # the vertices
        self._vertices = vertices  # type: List[Vector]

    @property
    def shape(self) -> b2.b2LoopShape:
        return b2.b2LoopShape(
            vertices=[(*v,) for v in self._vertices]
        )


if __name__ == '__main__':
    class Player(BaseEntity):
        pass


    p = Player()
    c = BoxCollider(box=Vector(20, 20))
    pc = PolygonCollider(vertices=[
        Vector(1, 1), Vector(2, 2), Vector(3, 3),
    ])
    print(c.entity)
    p.addComponent(c)
    print(c.entity)
    print(c.isSensor)
