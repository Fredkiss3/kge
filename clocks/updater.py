# import asyncio
import threading
import time
import traceback
from typing import Callable
from concurrent import futures
from typing import Any, Union

import pyglet

import kge
from kge.core import events
from kge.core.events import Event
from kge.core.constants import DEFAULT_FPS
from kge.core.system import System


class Updater(System):

    def __init__(self, engine=None, time_step=1 / DEFAULT_FPS, **kwargs):
        super().__init__(engine, **kwargs)
        self.accumulated_time = 0
        self.last_tick = None
        self.start_time = None
        self.time_step = time_step
        self.event_to_dispatch = events.Update
        self.after_event = events.LateUpdate
        self.updating = False

    def __enter__(self):
        pyglet.clock.schedule_interval_soft(self.update_entities, self.time_step)
        self.start_time = time.monotonic()

    def update_entities(self, time_delta: float,
                        # dispatch: Callable[[Event], None], scene: "kge.Scene"
                        ):
        dispatch = self._dispatch
        scene = self.engine.current_scene
        if self.engine.running:
            event = self.event_to_dispatch.__call__(time_delta, scene)  # type: Union[events.Update, events.FixedUpdate]
            scene.main_camera.__fire_event__(event, dispatch)

            # print(len(list(event.scene)))
            for e in event.scene:
                if self.engine.running:
                    # if scene.main_camera.in_frame(e):
                        # Instead of submitting jobs, which can take a huge amount of time to process
                        # Just run the update method
                        # print(f"Updating entity : {e}")
                        e.__fire_event__(event, dispatch)
                else:
                    break

            # then dispatch late update
            if self.engine.running:
                if isinstance(event, events.Update):
                    dt = event.delta_time
                else:
                    dt = event.fixed_delta_time
                self._dispatch(self.after_event.__call__(delta_time=dt, scene=event.scene))

    # def on_idle(self, dt, event: events.SceneStarted = None, dispatch: Callable[[Event], None] = None):
    #     if self.engine.running:
    #         # print(event, "On thread : ", threading.current_thread())
    #         if self.last_tick is None:
    #             self.last_tick = time.monotonic()
    #         this_tick = time.monotonic()
    #         self.accumulated_time += this_tick - self.last_tick
    #         self.last_tick = this_tick
    #
    #         while self.accumulated_time >= self.time_step:
    #             # This might need to change for the Idle event system to dispatch _only_ once per idle event.
    #             self.accumulated_time += -self.time_step
    #
    #             # if idle_event.scene:
    #             #     self._executor.submit(self.dispatch_to_entities, idle_event, dispatch)
    #             if self.engine.running and not self.updating:
    #                 # We don't need to run two updates at the same time
    #                 self.updating = True
    #                 # print("Updating entities")
    #                 self.update_entities(self.time_step * self.engine.time_scale, self._dispatch,
    #                                      self.engine.current_scene)
    #                 # print("Finished Updating")
    #                 self.updating = False
