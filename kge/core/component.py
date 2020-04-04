from typing import Callable

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
                if not self._initialized and not isinstance(event, events.SceneStopped) and \
                        not isinstance(event, events.Init):
                    # Initialize the component
                    super(BaseComponent, self).__fire_event__(events.Init(scene=event.scene), dispatch)
                    self._initialized = True

                # fire event
                super(BaseComponent, self).__fire_event__(event, dispatch)
                if isinstance(event, events.Init) and not self._initialized:
                    self._initialized = True

    def on_scene_stopped(self, ev, dispatch):
        self._initialized = False

    def __init__(self, entity=None):
        if entity is not None:
            if not isinstance(entity, kge.Entity):
                raise TypeError("entity should be of type 'kge.Entity' or a subclass of 'kge.Entity'")
        self.entity = entity  # type: kge.Entity

        # Used to Initialize component
        self._initialized = False

        # Used to tell if the component is active
        self.is_active = True

    def __repr__(self):
        return f"component {type(self).__name__} of entity '{self.entity}'"


Component = BaseComponent
