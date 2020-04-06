from typing import Callable

from kge.core import events
from kge.core.system import System
from kge.physics.events import PhysicsUpdate


class EventDispatcher(System):
    """
    The system that is responsible for dispatching events to entities
    """

    def __fire_event__(self, event: events.Event, dispatch: Callable[[events.Event], None]) -> None:
        if self.engine.running and not isinstance(event, (events.Update, events.FixedUpdate, PhysicsUpdate)):
            if event.scene is not None:
                if type(event).__name__ in event.scene.registered_events:
                    if event.onlyEntity is None:

                        # Get Registered entities for event
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
