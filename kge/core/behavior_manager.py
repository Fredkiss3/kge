from typing import Callable

from kge.core import events
from kge.core.behaviour import Behaviour
from kge.core.component_system import ComponentSystem
from kge.core.events import Event


class BehaviourManager(ComponentSystem):
    """
    The system that handles behaviors a.k.a "Scripts"
    """
    def __init__(self, engine, **_):
        super().__init__(engine, **_)
        self.components_supported = (Behaviour,)

    def __fire_event__(self, event: Event, dispatch: Callable[[Event], None]) -> None:
        super(BehaviourManager, self).__fire_event__(event, dispatch)

        event_name = type(event).__name__
        if event_name in self.event_map:
            components = self.event_map[event_name]
            if event.scene:
                if event.onlyEntity is None:
                    for behavior in components:
                        if self.engine.running:
                            behavior.__fire_event__(event, dispatch)
                        else:
                            # Break if the engine has finished running
                            break
                else:
                    # get the behaviors concerned by the event and the entity
                    concerned = filter(lambda c: c.entity == event.onlyEntity, components)
                    for behavior in concerned:
                        behavior.__fire_event__(event, dispatch)
