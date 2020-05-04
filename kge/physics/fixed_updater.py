from kge.clocks.updater import Updater
from kge.core import events
from kge.core.constants import FIXED_FPS


class FixedUpdater(Updater):
    """
    Updater for physics systems
    """

    def __init__(self, **kwargs):
        super().__init__(time_step=1 / (FIXED_FPS ), **kwargs)
        self.event_to_dispatch = events.FixedUpdate
        self.after_event = events.PhysicsUpdate
