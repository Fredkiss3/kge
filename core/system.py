import asyncio
from concurrent import futures
from typing import Union, Deque, Iterable, Optional, Callable, Any
# from copy import deepcopy

import kge
from kge.core import events
from kge.core.eventlib import EventMixin
from kge.core.events import Event
from kge.core.logger import LoggerMixin

# import threading


class System(EventMixin, LoggerMixin,
             # threading.Thread
             ):
    """
    a system is an object that handles events
    """

    def __init__(self, engine=None, **_):
        super().__init__()
        self.engine = engine  # type: kge.Engine
        self._dispatch = None  # type: Union[Callable[[Event, bool], None], None]
        if self.engine:
            self._dispatch = self.engine.dispatch

        # REMOVED !
        # self.running = False  # if the system is running
        self._last_idle_time = None  # last time the engine did update

        # REMOVED !
        # self.event_queue = deque()
        # self.next_event_queue = deque()
        self.async_loop = None  # type: Optional[asyncio.AbstractEventLoop]
        self._executor = futures.ThreadPoolExecutor()  # type: futures.thread.ThreadPoolExecutor


    def __fire_event__(self, event: Event, dispatch: Callable[[Event], None]) -> None:
        if self.engine.running:
            super(System, self).__fire_event__(event, dispatch)

    # def on_quit(self, event, dispatch):
    #     """
    #     Shutdown executor in order to finish
    #     """
    #     self._executor.shutdown(wait=False)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # REMOVED !
        # self.running = False
        pass

    # REMOVED !
    # def enqueue(self, next_queue: Iterable[Event] = None, current_queue: Iterable[Event] = None):
    #     """
    #     Enqueue a queue to self
    #     """
    #     if next_queue is not None:
    #         self.next_event_queue.extend(list(next_queue))
    #     if current_queue is not None:
    #         self.event_queue.extend(list(current_queue))

    # def on_quit(self, event, dispatch):
    #     self.running = False

    @staticmethod
    async def run_func_in_async_mode(callback: Callable[[Any], None], *args):
        """
        Run callback in async mode
        """
        # Sleep in order to let other tasks get processed
        await asyncio.sleep(0.0001)
        # Launcb Callback with provided args
        callback(*args)

    # REMOVED !
    # def run(self):
    #     """
    #     Run the thread
    #     """
    #     self.running = True
    #     self._last_idle_time = time.monotonic()
    #
    #     while self.running:
    #         try:
    #             # Get time_delta
    #             now = time.monotonic()
    #             time_delta = now - self._last_idle_time
    #             self._last_idle_time = now
    #
    #             # Enque idle event
    #             self.enqueue([events.Idle(time_delta, scene=self.engine.current_scene)])
    #
    #             # get last events added to the queue
    #             self.event_queue.extend(self.next_event_queue)
    #             self.next_event_queue = deque()
    #
    #             # Dispatch events to queue
    #             while self.event_queue:
    #                 event = self.event_queue.popleft()
    #                 self.__fire_event__(event, self._dispatch)
    #
    #         except Exception as e:
    #             # If an error occurs, shut down the system
    #             self.logger.error(f"A Fatal Exception Happened : {e} \nshutting down {type(self).__name__}...")
    #             self.running = False
    #             break
    #         else:
    #             pass
    #
    #     self.logger.info(f"The system {type(self).__name__} ended.")