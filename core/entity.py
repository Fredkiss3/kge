import traceback
from typing import List, Union, Type, Dict, Tuple, Callable, TypeVar

import kge
from kge.utils.vector import Vector
from kge.core import events
from kge.core.component import Component
from kge.core.eventlib import EventMixin

from copy import deepcopy

from kge.core.events import Event
from kge.core.transform import Transform
from kge.utils.dotted_dict import DottedDict

# Anything
T = TypeVar("T")


class BaseEntity(EventMixin):
    """
    An entity is a game object that can be used in the game engine

    In order to add a behavior to an entity (like moving the player for example),
    we must use event handlers.
    Their signatures are :

    def on_{event_name}(self, event_type, dispatch_function):
        (your code goes here)

    Where :
        - event_name is the name of the event in snake_case
        - dispatch_function is a function to call in order to send messages, in practice, you won't use it so much

    Example of an event handler :

        >>> class Player(Entity):
        >>>     def on_update(self, event, dispatch):
        >>>         print("Updating the player...")

    If you want to know a list of all events, you should see in module ``kge.core.events``

    """
    # Number of items created for that type
    nbItems = 0

    def __fire_event__(self, event: Event, dispatch: Callable[[Event], None]):
        if event.scene is not None:
            if event.scene.engine.running:
                if self._initialized == False and not isinstance(event, events.SceneStopped):
                    # Initialize the entity
                    super(BaseEntity, self).__fire_event__(events.Init(scene=event.scene), dispatch)
                    self._initialized = True

                try:
                    super(BaseEntity, self).__fire_event__(event, dispatch)
                #
                #     if event.scene.engine.running:
                #         # Propagate event to components before self
                #         for key in list(self._components):
                #             component = self._components[key]
                #             if event.scene.engine.running:
                #                 component.__fire_event__(event, dispatch)
                #             else:
                #                 break
                except Exception:
                    print(
                        f"An Error Happened in {self} (Components : {self._components}) for event : {event}. ")
                    traceback.print_exc()

    def on_add_component(self, ev: events.AddComponent, dispatch):
        """
        Add a component to this entity
        NEVER TRY TO SUBCLASS THIS Method !!!
        """
        self.addComponent(key=ev.key, component=ev.component)

    def on_remove_component(self, ev: events.RemoveComponent, dispatch):
        """
        Remove a component from this entity
        NEVER TRY TO SUBCLASS THIS Method !!!
        """
        cp = self.removeComponent(ev.kind)  # type: List[Component]

    def on_scene_stopped(self, ev, dispatch):
        self._initialized = False

    def __init__(self, name: str = None, tag: str = None):
        if (tag is not None and not isinstance(tag, str)) or (name is not None and (not isinstance(name, str))):
            raise TypeError("name and tags should be strings")

        type(self).nbItems += 1

        # if the object does not need to receive any kind of events
        self.static = False

        # The components attached to the object
        self._components = {}  # type: Dict[str, Component]
        self.name = self.name = f"new {type(self).__name__} {type(self).nbItems}"
        self._tag = tag

        # is this entity initialized ?
        self._initialized = False

        # Set the name and tags of the entity
        if name is not None:
            self.name = name

        # the scene in which this entity is in
        self.scene = None  # type: #Union[BaseScene, None]

        # children and parent
        self._children = []  # type: List[BaseEntity]
        self._parent = None  # type: Union[BaseEntity, None]

        # is active ? (if False, it will not render)
        self._is_active = True

        # the layer in which the entity is in
        self.layer = 0

        # transform of the entity
        self._transform = Transform(entity=self)
        self.destoyed = False

    @property
    def size(self) -> DottedDict:
        """
        Size of the entity (should be subclassed)
        and must return a dottedDict in form :
            >>> DottedDict(width=..., height=...)

        :return:
        """
        return DottedDict(width=0, height=0)

    @property
    def left(self):
        """
        Left world position in units

        :return:
        """
        return (self.position.x - self.size.width / 2) * abs(self.transform.scale.x)

    @property
    def right(self):
        """
        right world position in units

        :return:
        """
        return (self.position.x + self.size.width / 2) * abs(self.transform.scale.x)

    @property
    def top(self):
        """
        Up world position in units

        :return:
        """
        return (self.position.y + self.size.height / 2) * abs(self.transform.scale.y)

    @property
    def bottom(self):
        """
        Down world position in units

        :return:
        """
        return (self.position.y - self.size.height / 2) * abs(self.transform.scale.y)

    @property
    def transform(self):
        return self._transform

    @property
    def position(self):
        return self._transform.position

    @position.setter
    def position(self, value: Union[Tuple[float, float], Vector]):
        self._transform.position = value

    @property
    def tag(self):
        return self._tag

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value: "BaseEntity"):
        if isinstance(value, BaseEntity):
            self._parent = value
            value.children.append(self)
            self._transform.parent = value.transform
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
        Get a copy of components of this entity
        """
        return dict(self._components)

    def getComponents(self, kind: Type[T]) -> Union[List[T]]:
        """
        get components of type given

        You can call it either with type (a subtype of component) to get all components
        of type given, that are in the entity :
            >>> player.getComponents(Transform)
            >>> [transform component1, transform component2]

        :param kind: the kind of component to retrieve
        :return:
        """
        if isinstance(kind, type):
            return [component for component in self._components.values() if isinstance(component, kind)]
        else:
            raise TypeError(
                "kind argument should be a type or a subtype of 'kge.Component'")

    def getComponent(self, kind: Union[Type[T], str]) -> Union[T, None]:
        """
        return the first component whose key is 'kind' or type is 'kind'.

        You can call it either with type (a subtype of component) to get one component
        of type given, that is in the entity :
            >>> t = player.getComponent(Transform)
            >>> print(t)
            >>> "Component Transform of entity Entity X"

        of with an string parameter to get directly the component you want to have:
            >>> t = player.getComponent("transform")
            >>> print(t)
            >>> "Component Transform of entity Entity X"

        :param kind: the kind of component to retrieve
        :return: the component requested or None if there is None
        """
        if isinstance(kind, type):
            cp = None
            for component in self._components.values():
                if isinstance(component, kind):
                    cp = component
                    break
            return cp
        elif isinstance(kind, str):
            try:
                return self._components[kind]
            except KeyError:
                return None
        else:
            return None

    def removeComponent(self, kind: Union[Type[T], str]) -> Union[List[T]]:
        """
        remove components of type given

        You can call it either with type (a subtype of component) to get all components
        of type given, that are in the entity :
            >>> player.removeComponent(PlayerMovement)
            >>> ["Component PlayerMovement of entity player", "Component PlayerMovement of entity player"]

        of with an string parameter to get directly the component you want to have:
            >>> player.removeComponent("player_movement")
            >>> ["Component PlayerMovement of entity player"]

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
        elif isinstance(kind, str):
            try:
                cp = self._components.pop(kind)
                cp.is_active = False

                # Dispatch component removed event
                manager = kge.ServiceProvider.getEntityManager()
                manager.dispatch_component_operation(self, [cp], added=False)
                return [cp]
            except KeyError:
                raise []
        else:
            raise TypeError(
                "kind must be a string or a subclass of 'kge.Component'")

    def addComponent(self, key: str, component: T):
        """ Add a component """

        if isinstance(component, Component):
            if isinstance(component, Transform):
                raise AttributeError(
                    "Cannot add transform manually to an entity")
            # set component entity and activate it
            component.entity = self
            component.is_active = True
            self._components[key] = component

            manager = kge.ServiceProvider.getEntityManager()
            manager.dispatch_component_operation(self, component, added=True)
        else:
            # must be a subtype of Component
            raise TypeError(
                f"{type(component)} is not a subtype of {Component}")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} ({type(self).__name__})"

    def __deepcopy__(self, memo=None):
        """
        Copy an instance of this object
        """
        entity = type(self)()
        entity.name = f"copy of {self.name}"
        entity.scene = self.scene
        entity._components = dict(self._components)
        entity.is_active = True
        entity._children = dict(self._children)
        entity._parent = deepcopy(self._parent)
        return entity

    def copy(self):
        """
        returns a copy of this entity
        """
        copy = deepcopy(self)
        return copy

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

        if val:
            self._activate()
        else:
            self._deactivate()

    def destroy(self):
        """
        Destroy this entity
        """
        manager = kge.ServiceProvider.getEntityManager()

        if manager:
            manager.destroy(self)
            # self.destoyed = True

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
            # self.destoyed = True

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
            # self.destoyed = True


Entity = BaseEntity

if __name__ == '__main__':
    # import time
    class Player(BaseEntity):
        pass


    class PlayerMovement(Component):
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
    player.addComponent("movement", PlayerMovement(player))
    player.addComponent("movement2", PlayerMovement(player))

    # print(c.transform)
    player.position = Vector(1, 1)
    player._transform.position = (5, 5)
    print(player._transform)
    print(player.getComponent(PlayerMovement))
    print(player.getComponent("movement"))

    player2 = player.copy()

    print(player2)
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
