from typing import Union, List, Callable
import kge
from kge.core import events
from kge.core.eventlib import EventMixin
from kge.core.events import Event


class BaseComponent(EventMixin):
    """
    A component represents an element that can be added to an entity
    to add a functionality
    """

    def __fire_event__(self, event: Event, dispatch: Callable[[Event], None]):
        """
        Initialize the component before everything
        """
        if event.scene is not None:
            if event.scene.engine.running:
                if self._initialized == False and not isinstance(event, events.SceneStopped):
                    # Initialize the component
                    super(BaseComponent, self).__fire_event__(events.Init(scene=event.scene), dispatch)
                    self._initialized = True

                # fire event
                super(BaseComponent, self).__fire_event__(event, dispatch)

    def on_scene_stopped(self, ev, dispatch):
        self._initialized = False

    def __init__(self, entity=None):
        if entity is not None:
            if not isinstance(entity, kge.Entity):
                raise TypeError("entity should be of type 'kge.Entity' or a subclass of 'kge.Entity'")
        self.entity = entity # type: kge.Entity

        # children and parent
        self._children = []  # type: List[BaseComponent]
        self._parent = None  # type: Union[BaseComponent, None]

        # Used to Initialize component
        self._initialized = False

        # Used to tell if the component is active
        self.is_active = True

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value: "BaseComponent"):
        if isinstance(value, BaseComponent):
            self._parent = value
            value.children.append(self)
        elif value is None:
            # remove self from children
            self._parent.children.remove(self)

            # set parent to None
            self._parent = None
        else:
            raise TypeError("parent Should be of type 'kge.Component' or a subclass of 'kge.Component'")

    def __repr__(self):
        return f"component {type(self).__name__} of entity '{self.entity}'"

Component = BaseComponent