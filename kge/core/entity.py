import traceback
from typing import List, Union, Type, Tuple, Callable, TypeVar, Optional, Set

import pyglet

import kge
from kge.core import events
from kge.core.component import BaseComponent
from kge.core.eventlib import EventMixin
from kge.core.events import Event
from kge.core.transform import Transform
from kge.utils.coroutine import coroutine, Coroutine
from kge.utils.dotted_dict import DottedDict
from kge.utils.vector import Vector

# Anything
T = TypeVar("T", bound=BaseComponent)


class BaseEntity(EventMixin):
    """
    An entity is a game object that can be used in the game engine

    In order to add a behavior to an entity (like moving the player for example),
    we must use event handlers and behaviours.

    Their signatures are :

    def on_{event_name}(self, event_type, dispatch_function):
        (your code goes here)

    Where :
        - event_name is the name of the event in snake_case
        - event_type is the event, you should use that, it contains a lot of important parameters
        - dispatch_function is a function to call in order to send custom events, in practice, you won't use it so much

    Example of an event handler :

        >>> class Player(Entity):
        >>>     def on_update(self, event, dispatch):
        >>>         print("Updating the player...")

    If you want to know a list of all events, you should see in module ``kge.core.events``
    """
    # Number of items created for that type
    nbItems = 0
    scene: "kge.Scene"
    _children: Set["BaseEntity"]
    _parent: Optional["BaseEntity"]
    vlist: pyglet.graphics.vertexdomain.VertexList
    xf_vlist: pyglet.graphics.vertexdomain.VertexList
    _order_in_layer: int
    coroutines: Set[Coroutine]

    def __fire_event__(self, event: Event, dispatch: Callable[[Event], None]):
        if event.scene is not None:
            if event.scene.engine.running:
                if self._initialized == False and not isinstance(event, events.SceneStopped) \
                        and not isinstance(event, events.Init):
                    # Initialize the entity
                    super(BaseEntity, self).__fire_event__(events.Init(scene=event.scene), dispatch)
                    self._initialized = True

                try:
                    super(BaseEntity, self).__fire_event__(event, dispatch)
                except Exception:
                    print(
                        f"""An Error Happened in {self} (Components : {list(
                            self.components.values())}) for event : {event}. """)
                    traceback.print_exc()
                else:
                    if isinstance(event, events.Init):
                        self._initialized = True

    def __new__(cls,
                *args,
                name: str = None,
                tag: str = None,
                **kwargs, ):
        if (tag is not None and not isinstance(tag, str)) or (name is not None and (not isinstance(name, str))):
            raise TypeError("name and tags should be strings")

        inst = super().__new__(cls)

        # Update number of items
        cls.nbItems += 1

        # The components attached to the object
        inst._components = {}
        inst.name = inst.name = f"new {type(inst).__name__} {cls.nbItems}"
        inst._tag = tag

        # is this entity initialized ?
        inst._initialized = False

        # Set the name and tags of the entity
        if name is not None:
            inst.name = name

        # the scene in which this entity is in
        inst.scene = None

        # children and parent
        inst._children = set()
        inst._parent = None

        # is active ? (if False, it will not render or receive events)
        inst._is_active = True

        # the layer in which the entity is in
        inst.layer = 0

        # order in layer
        # TODO : REVIEW
        inst.layer_order = 0

        # transform of the entity
        inst._transform = Transform(entity=inst)
        inst.destroyed = False

        # vertex lists for debug draw
        inst.vlist = None
        inst.xf_vlist = None

        # Coroutines
        inst.coroutines = set()

        return inst

    @property
    def layer_order(self):
        """
        Get layer order of the entity,
        there are only 510 layers, so make sure to not go over
        TODO : REVIEW
        """
        return self._order_in_layer + 255

    @layer_order.setter
    def layer_order(self, val: int):
        # TODO : REVIEW
        if not isinstance(val, (int, float)):
            raise TypeError("Layer Order should be a number")

        self._order_in_layer = int(val) - 255

    def flipX(self):
        self.transform.scale.x = -self.transform.scale.x

    def flipY(self):
        self.transform.scale.y = -self.transform.scale.y

    @property
    def debuggable(self):
        """
        This property is used to mark an entiy as to be re-rendered on debug
        """
        if self.scene is None:
            return False
        else:
            return self in self.scene.debuggable

    @debuggable.setter
    def debuggable(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("Only boolean values allowed for 'debuggable' Flag")
        if self.scene is not None:
            if val:
                self.scene.mark_as_debuggable(self)
            elif self.debuggable:
                self.scene.debuggable.remove(self)

    @property
    def dirty(self):
        """
        This property is used to mark an entiy as to be re-rendered
        """
        if self.scene is None:
            return False
        else:
            return self in self.scene.dirties

    @dirty.setter
    def dirty(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("Only boolean values allowed for 'dirty' Flag")
        if self.scene is not None:
            if val:
                self.scene.mark_as_dirty(self)
            elif self.dirty:
                self.scene.dirties.remove(self)

    @property
    def size(self) -> DottedDict:
        """
        Size of the entity (should be subclassed)
        and must return a dottedDict in form :
            >>> DottedDict(width=..., height=...)

        :return:
        """
        return DottedDict(width=abs(self.transform.scale.x), height=abs(self.transform.scale.y))

    @property
    def transform(self):
        # set position and angle
        rb = self.getComponent(kind=kge.RigidBody)
        if rb is not None:
            if rb.body is not None:
                self._transform.angle = rb.angle
                self._transform.position = rb.position
        return self._transform

    @property
    def position(self):
        # If there is a rigidBody
        rb = self.getComponent(kind=kge.RigidBody)

        if rb is not None:
            if rb.body is not None and self._transform.position != rb.position:
                if not isinstance(self, kge.Camera):
                    if self.scene is not None:
                        self.scene.spatial_hash.remove(self._transform.position,
                                                       Vector(self.size.width, self.size.height),
                                                       self)
                        self.scene.spatial_hash.add(rb.position, Vector(self.size.width, self.size.height), self)

                    # When position get changed, mark as 'dirty'
                    self.dirty = True
                    self.debuggable = True
                self._transform.position = rb.position
        return self._transform.position

    @position.setter
    def position(self, value: Vector):
        if self._transform.position != value:
            rb = self.getComponent(kind=kge.RigidBody)

            # Set position of the body
            if rb is not None:
                rb.position = Vector(value)

            if self.scene is not None:
                # set as dirty
                self.dirty = True
                self.debuggable = True

                self.scene.spatial_hash.remove(self._transform.position, Vector(self.size.width, self.size.height),
                                               self)
                self.scene.spatial_hash.add(value, Vector(self.size.width, self.size.height), self)

            self._transform.position = Vector(value)

    @property
    def scale(self):
        """
        Get the scale of the entity
        """
        return self._transform.scale

    @scale.setter
    def scale(self, value: Union[Tuple[float, float], Vector]):
        """
        Set the scale of the entity
        """
        if self.scale != value:
            self.dirty = True
            self.debuggable = True
        self._transform.scale = value

    @property
    def angle(self):
        """
        Get angle, in degrees
        """
        rb = self.getComponent(kind=kge.RigidBody)
        if rb is not None:
            if rb.body is not None:
                self.dirty = True
                if rb.angle != self._transform.angle:
                    self.dirty = True
                    self.debuggable = True
                    self._transform.angle = rb.angle
        return self._transform.angle

    @angle.setter
    def angle(self, value: float):
        """
        Set angle, in degrees
        """
        rb = self.getComponent(kind=kge.RigidBody)

        # Set position of the body
        if rb is not None:
            rb.angle = value

        if value != self._transform.angle:
            self.dirty = True
            self.debuggable = True
        self._transform.angle = value

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, val: str):
        self._tag = val

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value: "BaseEntity"):
        if isinstance(value, BaseEntity):
            if value.parent is not self:
                if self._parent is not None:
                    self._transform.parent = None
                    self._parent.children.remove(self)

                self._parent = value
                value.children.add(self)
                self._transform.parent = value.transform
            else:
                raise ValueError(f"{value} cannot be parent of {self} because {self} is already the parent of {value}")
        elif value is None:
            # remove self from children
            self._parent.children.remove(self)

            # set parent to None
            self._parent = None

            # remove transform constraint
            self._transform.parent = None
        else:
            raise TypeError("Value Must be an Entity or a subclass of Entity")

    @property
    def components(self):
        """
        Get a list of components of this entity
        """
        return self._components

    def start_coroutine(self, func: Callable, delay: float = .01, loop: bool = False, *args, **kwargs):
        """
        TODO: Reformat Coroutines to generators function
        Start a coroutine

        when setting a function as coroutine, your function should not have an infinite loop in it
        if there is one, it will freeze your game
        instead use loop argument in order to loop your function and use delay argument to defer the call to your function

        Coroutines return nothing.

        Example of use :
            >>> class Player:
            >>>     def yodele(self, name)
            >>>         print("YODELE", name, "!")
            >>>
            >>>     def call_yodele(self, name):
            >>>         self.start_coroutine(self.yodele, name="Fred")
            >>>
            >>> p = Player()
            >>> p.call_yodele("hi hou !")
            >>> Output : "YODELE hi hou !"

        """
        c = coroutine(func, delay, loop)
        c(*args, **kwargs)

        # add coroutines
        manager = kge.ServiceProvider.getEntityManager()
        manager.addCoroutine(self, c)
        self.coroutines.add(c)

    # def on_stop_scene(self, event: Event, dispatch: Callable[[Event], None]):
    #     """
    #     When scene get stopped, destroy self
    #     """
    #     print("Stop Scene")
    #     self.on_destroy_entity(event, dispatch)

    # def on_destroy_entity(self, event, dispatch):
    #     """
    #     When entity gets destroyed,
    #     pay attention when subclassing, you could break default behaviours
    #     """
    #     # Remove parent-child relation
    #     if self.parent is not None:
    #         self.parent.children.remove(self)
    #         self.parent = None
    #     for coroutine in self._coroutines:
    #         coroutine.stop_loop()

    def getComponents(self, kind: Type[T]) -> Union[List[T]]:
        """
        get components of type given

        You can call it either with type (a subtype of component) to get all components
        of type given, that are in the entity :
            >>> player.getComponents(Transform)
            >>> ["transform component1", "transform component2"]

        :param kind: the kind of component to retrieve
        :return:
        """
        if isinstance(kind, type):
            return [component for component in self._components.values() if isinstance(component, kind)]
        else:
            raise TypeError(
                "kind argument should be a type or a subtype of 'kge.BaseComponent'")

    def getComponent(self, kind: Type[T]) -> Union[T, None]:
        """
        return the first component whose key is 'kind' or type is 'kind'.

        You can call it either with type (a subtype of component) to get one component
        of type given, that is in the entity :
            >>> t = player.getComponent(Transform)
            >>> print(t)
            >>> "BaseComponent Transform of entity Entity X"

        :param kind: the kind of component to retrieve
        :return: the component OF type requested or None if there is no component of type requested
        """
        if isinstance(kind, type):
            cp = None
            for component in self._components.values():
                if isinstance(component, kind):
                    cp = component
                    break
            return cp
        else:
            return None

    def removeComponent(self, kind: Union[Type[T]]) -> Union[List[T]]:
        """
        remove components of type given

        You can call it either with type (a subtype of component) to get all components
        of type given, that are in the entity :
            >>> player.removeComponent(PlayerMovement)
            >>> ["BaseComponent PlayerMovement 1 of entity player", "BaseComponent PlayerMovement 2 of entity player"]

        :param kind: the kind of component to retrieve
        """
        if isinstance(kind, type):
            cp = [(k, component) for k, component in self._components.items() if
                  isinstance(component, kind)]

            for k, c in cp:
                cp_ = self._components.pop(k)
                cp_.is_active = False

            cp = list(filter(lambda c: c[1], cp))  # type: List[T]

            # Dispatch component removed event
            manager = kge.ServiceProvider.getEntityManager()
            manager.dispatch_component_operation(self, cp, added=False)
            return cp
        else:
            raise TypeError(
                "kind must be or a subclass of 'kge.BaseComponent or kge.Behaviour'")

    def addComponents(self, *components: T):
        for c in components:
            self.addComponent(c)

    def addComponent(self, component: T):
        """ Add a component """

        if isinstance(component, BaseComponent):
            if isinstance(component, Transform):
                raise AttributeError(
                    "Cannot add transform manually to an entity")

            # set component entity and activate it
            key = hash(component)
            component.entity = self
            component.is_active = True
            self._components[key] = component

            manager = kge.ServiceProvider.getEntityManager()
            manager.dispatch_component_operation(self, component, added=True)
        else:
            # must be a subtype of BaseComponent
            raise TypeError(
                f"{type(component)} is not a subtype of {BaseComponent}")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} ({type(self).__name__})"

    def __iter__(self):
        return (component for component in self._components)

    def __destroy(self):
        """
        Destroy this entity
        """
        self.nbItems -= 1
        self.scene = None
        self._parent = None
        self._is_active = False
        for child in self._children:
            child.__destroy()

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("Is active should be a bool !")

        if val != self._is_active:
            self._is_active = val
            self.dirty = True
            self.debuggable = True

        if val:
            self._activate()
        else:
            self._deactivate()

    def destroy(self):
        """
        Destroy this entity
        """
        self.is_active = False

        manager = kge.ServiceProvider.getEntityManager()

        if manager:
            manager.destroy(self)

    def _deactivate(self):
        """
        Deactivate
        """
        self._is_active = False

        # Deactivate also components
        for cp in self._components.values():
            cp.is_active = False

        manager = kge.ServiceProvider.getEntityManager()

        if manager:
            manager.disable(self)

    def _activate(self):
        """
        Activate
        """
        self._is_active = True

        # Activate also components
        for cp in self._components.values():
            cp.is_active = True
        manager = kge.ServiceProvider.getEntityManager()

        if manager:
            manager.enable(self)
            # self.destroyed = True


Entity = BaseEntity

if __name__ == '__main__':
    # import time
    class Player(BaseEntity):
        pass


    class PlayerMovement(BaseComponent):
        pass


    player = Player(name="Player", tag="player")
    # last_idle = time.monotonic()
    # while True:
    #     now = time.monotonic()
    #     time_delta = now - last_idle
    #     last_idle = now
    # c.__fire_event__(events.Update(0.5), None)
    # time.sleep(0)
    # print(player.tags)
    player.addComponent(PlayerMovement(player))
    player.addComponent(PlayerMovement(player))

    # print(c.transform)
    player.position = Vector(1, 1)
    player._transform.position = (5, 5)
    print(player._transform)
    print(player.getComponent(PlayerMovement))

    # player2 = player.copy()

    # print(player2)
    print(player)
    # ev = deque()
    # ev.append(5)
    # ev.append(5)
    # ev.append(5)

    # def f(e):
    #     e.append(15)
    #
    # while ev:
    #     # ev.append(1)
    #     print(ev.popleft())
    #     f(ev)
