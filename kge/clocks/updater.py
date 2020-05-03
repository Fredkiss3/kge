import time
from typing import Union

import pyglet

from kge.core import events
from kge.core.constants import DEFAULT_FPS
from kge.core.system import System


class Updater(System):
    def __init__(self, engine=None, time_step=1 / (DEFAULT_FPS), **kwargs):
        super().__init__(engine, **kwargs)
        self.event_to_dispatch = events.Update
        self.after_event = events.LateUpdate

        self.time_step = time_step

    def __enter__(self):
        pyglet.clock.schedule_interval_soft(
            self.update, self.time_step)

    def update(self, dt):
        self.engine.append_job(
            self.update_entities, dt
        )
        # self.update_entities(dt)

    def update_entities(self, time_delta: float):
        start = time.monotonic()
        dispatch = self._dispatch
        scene = self.engine.current_scene
        if self.engine.running:
            event = self.event_to_dispatch.__call__(time_delta, scene)  # type: Union[events.Update, events.FixedUpdate]

            # Dispatch to behaviours
            self._dispatch(event)

            # Get registered entities for event
            entities = event.scene.registered_entities(event)

            for e in entities:
                if self.engine.running:
                    e.__fire_event__(event, dispatch)
                else:
                    break

            # then dispatch late update
            if self.engine.running:
                if isinstance(event, events.Update):
                    dt = event.delta_time
                else:
                    dt = event.fixed_delta_time

                # add the time elapsed in the loop
                dt += time.monotonic() - start
                self._dispatch(self.after_event.__call__(
                    delta_time=dt, scene=event.scene))
