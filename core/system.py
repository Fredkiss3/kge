import asyncio
from concurrent import futures
from typing import Union, Optional, Callable, Any

import kge
from kge.core.eventlib import EventMixin
from kge.core.events import Event
from kge.core.logger import LoggerMixin


class System(EventMixin, LoggerMixin):
    """
    a system is an object that handles events
    """

    def __init__(self, engine=None, **_):
        super().__init__()
        self.engine = engine  # type: kge.Engine
        self._dispatch = None  # type: Union[Callable[[Event, bool], None], None]

        # FIXME : to test
        # If the system must be running on its own thread
        self.require_thread = False

        if self.engine:
            self._dispatch = self.engine.dispatch

    def __fire_event__(self, event: Event, dispatch: Callable[[Event], None]) -> None:
        if self.engine.running:
            super(System, self).__fire_event__(event, dispatch)

    def __repr__(self):
        return type(self).__name__

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
