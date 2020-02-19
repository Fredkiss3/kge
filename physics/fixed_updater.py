import asyncio

from kge.clocks.updater import Updater
from kge.core import events
from kge.physics import events as p_events


class FixedUpdater(Updater):
    """
    Updater for physics systems
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_step = .02
        self.event_to_dispatch = events.FixedUpdate
        self.after_event = p_events.PhysicsUpdate
