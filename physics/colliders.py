from typing import Union, Callable, List, Optional

import pyglet

import kge
from kge.physics.rigid_body import RigidBody, RigidBodyType
from kge.utils.vector import Vector
from kge.core import events
from kge.core.component import BaseComponent
from kge.core.entity import BaseEntity
import Box2D as b2

from kge.core.events import Event
from kge.physics.events import BodyCreated, BodyDestroyed, CreateBody


class Collider(BaseComponent):
    """
    The only component that handles collisions
    and can collide with other colliders
    """

    def __init__(self,
                 isSensor: bool = False,
                 offset: Vector = Vector.Zero(),
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1,
                 ):
        super().__init__(None)
        if not isinstance(isSensor, bool):
            raise TypeError("Sensor should be a bool")

        # does this collider pass through objects ?
        self.isSensor = isSensor

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
    def rigid_body_attached(self):
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

        body.CreateFixture(b2.b2FixtureDef(
            density=self.density,
            restitution=self.bounciness,
            isSensor=self.isSensor,
            shape=self.shape,
            friction=self.friction,
            userData=self
        ))

        # our fixture is the last
        self._fixture = body.fixtures[-1]  # type: b2.b2Fixture

    ############################
    #         Events           #
    ############################

    def on_body_created(self, ev: BodyCreated, dispatch):
        if ev.entity == self.entity:
            rb = self.entity.getComponent(kind=RigidBody)  # type: RigidBody
            if rb is not None:
                self._rb = rb

            # create a fixture for this body
            if self._fixture is None:
                self.__create(body=ev.body)

    def on_body_destroyed(self, ev: BodyDestroyed, dispatch):
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
                body_component=rb
            )

            event.onlyEntity = self.entity
            dispatch(event)


class BoxCollider(Collider):
    """
    A component that handles collision in a box shape
    """

    def __init__(self,
                 box: Vector = None,
                 isSensor: bool = False,
                 offset: Vector = Vector.Zero(),
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1, ):
        """
        initialize the collider

        :param box: a vector which describes the box of the collider in form of Vector(width, height) default is set to entity size
        :param offset: The position of the collider relative to the parent body
        """
        super().__init__(isSensor, offset, bounciness, friction, density)

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
                 isSensor: bool = False,
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
        super().__init__(box, isSensor, offset, bounciness, friction, density)

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
                 isSensor: bool = False,
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1.0,
                 ):
        """
        initialize the collider

        :param radius: the radius of the collider
        :param center: The position of the center of the collider relative to the parent body
        """
        super().__init__(isSensor, center, bounciness, friction, density)

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


class PolygonCollider(Collider):
    """
    A component that handles collision within in a polygon shape
    FIXME : ADD A WAY TO AVOID ERRORS
    """

    def __init__(self,
                 vertices: List[Vector],
                 isSensor: bool = False,
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
        super().__init__(isSensor, Vector.Zero(), bounciness, friction, density)

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

    def __init__(self, vertices: List[Vector] = None, center: Vector = Vector.Zero(), isSensor: bool = False,
                 bounciness: float = 0,
                 friction: float = 0, density: float = 1.0):
        """
        initialize the collider

        :param center: The position of the center of the collider relative to the parent body
        :param p1: the first point of the triangle
        :param p2: the second point of the triangle
        :param p3: the third point of the triangle
        """
        super().__init__(isSensor, center, bounciness, friction, density)

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


class EdgeCollider(Collider):
    """
    A component that handles collisions which occurs in a line segment shape
    """

    def __init__(self,
                 vertices: List[Vector],
                 isSensor: bool = False,
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1,
                 ):
        """
        initialize the collider

        :param vertices: a list of points of the collider in this form :
            # each point is relative to the parent body
            >>> collider = EdgeCollider(
            >>>     vertices=[
            >>>         Vector(-1, -1), Vector(1, 1)
            >>> ])
        """
        super().__init__(isSensor, Vector.Zero(), bounciness, friction, density)

        if 2 <= len(vertices) <= 4:
            # the vertices
            self._vertices = vertices[:4]  # type: List[Vector]
        else:
            raise ValueError("Expected from 2 to 4 vertices.")

    @property
    def shape(self) -> b2.b2EdgeShape:
        return b2.b2EdgeShape(
            vertices=[(*v,) for v in self._vertices]
        )


class LoopCollider(Collider):
    """
    A component that handles collisions which occurs in a sequence of line segments that forms a circular list.
    """

    def __init__(self,
                 vertices: List[Vector],
                 isSensor: bool = False,
                 bounciness: float = 0,
                 friction: float = 0,
                 density: float = 1,
                 ):
        """
        initialize the collider. When you give vertices, the collider automatically closes itself with the
        last vertex and first vertex forming a segment. This collider accept inside and outside collisions

        :param vertices: a list of points of the collider in this form :
            # each point is relative to the parent body
            >>> collider = EdgeCollider(
            >>> vertices=[
            >>>   Vector(-1, -1), Vector(2, 2), Vector(1, 1)
            >>> ])
        """
        super().__init__(isSensor, Vector.Zero(), bounciness, friction, density)

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
    p.addComponent("collider1", c)
    print(c.entity)
    print(c.isSensor)
