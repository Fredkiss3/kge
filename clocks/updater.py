import time
import traceback
from typing import Union

import pyglet


import threading
import kge
from kge.core import events
from kge.core.constants import DEFAULT_FPS
from kge.core.system import System


class Updater(System):

    def __init__(self, engine=None, time_step=1 / DEFAULT_FPS, **kwargs):
        super().__init__(engine, **kwargs)
        self.event_to_dispatch = events.Update
        self.after_event = events.LateUpdate
        self.require_thread = False

        self.accumulated_time = 0
        self.last_tick = None
        self.time_step = time_step

    def __enter__(self):
        if not self.require_thread:
            pyglet.clock.schedule_interval(self.update_entities, self.time_step)

    def start(self):
        """
        Start the system in its own thread
        """
        print(f"Started on thread : {threading.current_thread()}")
        while self.engine.running:
            if self.last_tick is None:
                self.last_tick = time.monotonic()
            this_tick = time.monotonic()
            self.accumulated_time += this_tick - self.last_tick
            self.last_tick = this_tick
            while self.accumulated_time >= self.time_step:
                self.accumulated_time += -self.time_step
                self.update_entities(self.time_step)

    def update_entities(self, time_delta: float,
                        # dispatch: Callable[[Event], None], scene: "kge.Scene"
                        ):
        # time.sleep(1)
        start = time.monotonic()
        dispatch = self._dispatch
        scene = self.engine.current_scene
        if self.engine.running:
            event = self.event_to_dispatch.__call__(time_delta, scene)  # type: Union[events.Update, events.FixedUpdate]

            # Dispatch to behaviours
            self._dispatch(event)

            entities = filter(lambda e: e.has_event(type(event)), event.scene.simulated())

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
                self._dispatch(self.after_event.__call__(delta_time=dt, scene=event.scene))
        # end = time.monotonic()
        # print(f"Elapsed in {type(self).__name__} : {end - start}")
