import asyncio
import threading
from concurrent import futures
from typing import Callable

from kge.core import events
from kge.core.system import System
from kge.resources.events import AssetLoaded


class EventDispatcher(System):
    """
    The system that is responsible for dispatching events to entities
    """

    def __fire_event__(self, event: events.Event, dispatch: Callable[[events.Event], None]) -> None:
        super(EventDispatcher, self).__fire_event__(event, dispatch)
        # if threading.current_thread() is threading.main_thread():
            # print("On Main THread !")
        if event.scene:
            # If event is 'AssetLoaded' then dispatch to all entities of the world
            if isinstance(event, AssetLoaded):
                for e in event.scene.all:
                    if self.engine.running:
                        # Instead of submitting jobs, which can take a huge amount of time to process
                        # Just run the event handler
                        e.__fire_event__(event, dispatch)
                    else:
                        # Break if the engine has finished running
                        break
            else:
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
