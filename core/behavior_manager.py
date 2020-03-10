from typing import Callable

from kge.core.behaviour import Behaviour
from kge.core.component_system import ComponentSystem
from kge.core.events import Event


class BehaviourManager(ComponentSystem):
    """
    The system that handles behaviors
    """

    def __init__(self, engine, **_):
        super().__init__(engine, **_)
        self.components_supported = [Behaviour]

    def __fire_event__(self, event: Event, dispatch: Callable[[Event], None]) -> None:
        super(BehaviourManager, self).__fire_event__(event, dispatch)

        if event.scene:
            if event.onlyEntity is None:
                components = filter(lambda c: c.has_event(type(event)) and not c.entity.static, self.active_components())

                for behavior in components:
                    if self.engine.running:
                        behavior.__fire_event__(event, dispatch)
                    else:
                        # Break if the engine has finished running
                        break
            else:
                # get the behaviors concerned by the event
                concerned = event.onlyEntity.getComponents(kind=Behaviour)
                for behavior in concerned:
                    behavior.__fire_event__(event, dispatch)
