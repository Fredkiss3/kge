import time
from typing import Callable

from kge.core import events
from kge.core.entity import Entity
from kge.core.system import System
from kge.physics.events import PhysicsUpdate
from kge.resources.events import AssetLoaded


class EventDispatcher(System):
    """
    The system that is responsible for dispatching events to entities
    """

    def __fire_event__(self, event: events.Event, dispatch: Callable[[events.Event], None]) -> None:
        if self.engine.running and not isinstance(event, (events.Update, events.FixedUpdate, PhysicsUpdate)):
            if event.scene:
                if type(event).__name__ in event.scene.registered_events:
                    if event.onlyEntity is None:

                        # entities = filter(lambda e: e.has_event(type(event)), event.scene)
                        entities = event.scene.registered_entities(event)

                        for e in entities:
                            if self.engine.running:
                                e.__fire_event__(event, dispatch)
                            else:
                                # Break if the engine has finished running
                                break
                    else:
                        if event.onlyEntity in event.scene.registered_entities(event):
                            event.onlyEntity.__fire_event__(event, dispatch)
