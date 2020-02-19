import asyncio
from concurrent import futures
from typing import Callable

from kge.core import events
from kge.core.system import System


class EventDispatcher(System):
    """
    The system that is responsible for dispatching events to entities
    """

    def __fire_event__(self, event: events.Event, dispatch: Callable[[events.Event], None]) -> None:
        super(EventDispatcher, self).__fire_event__(event, dispatch)
        if event.scene:
            if event.onlyEntity is None:
                for e in event.scene:
                    if self.engine.running:
                        # Instead of submitting jobs, which can take a huge amount of time to process
                        # Just run the event handler
                        e.__fire_event__(event, dispatch)
                    else:
                        # Break if the engine has finished running
                        break
            else:
                event.onlyEntity.__fire_event__(event, dispatch)
