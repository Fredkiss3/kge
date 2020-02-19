# import asyncio
import time
import traceback
from typing import Callable
from concurrent import futures
from typing import Any, Union

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
        self.start_time = time.monotonic()


    def update_entities(self, time_delta: float, dispatch: Callable[[Event], None], scene: "kge.Scene"):
        if self.engine.running:
            event = self.event_to_dispatch.__call__(time_delta, scene)  # type: Union[events.Update, events.FixedUpdate]
            scene.main_camera.__fire_event__(event, dispatch)

            for e in event.scene:
                if self.engine.running:
                    # Instead of submitting jobs, which can take a huge amount of time to process
                    # Just run the update method
                    # print(f"Updating entity : {e}")
                    e.__fire_event__(event, dispatch)
                    # print(f"Entity Finsihed Updating : {e}")
                else:
                    # Break if the engine has finished running
                    break
                    # jobs.append(self._executor.submit())
                    # # jobs = self._executor.map(lambda e: e.__fire_event__(event, dispatch), event.scene)
                    # # Wait For completion
                    # for job in futures.as_completed(jobs):
                    #     try:
                    #         if self.engine.running:
                    #             data = job.result()
                    #     except Exception as e:
                    #         print(f'An Exception Happened : {e}')
                    #         traceback.print_exc()
                    #         self._executor.shutdown()

            # then dispatch late update
            if self.engine.running:
                if isinstance(event, events.Update):
                    dt = event.delta_time
                else:
                    dt = event.fixed_delta_time
                self._dispatch(self.after_event.__call__(delta_time=dt, scene=event.scene))

    def on_idle(self, idle_event: events.Idle, dispatch: Callable[[Event], None]):
        if self.last_tick is None:
            self.last_tick = time.monotonic()
        this_tick = time.monotonic()
        self.accumulated_time += this_tick - self.last_tick
        self.last_tick = this_tick

        if self.engine.running:
            while self.accumulated_time >= self.time_step:
                # This might need to change for the Idle event system to dispatch _only_ once per idle event.
                self.accumulated_time += -self.time_step

                # if idle_event.scene:
                #     self._executor.submit(self.dispatch_to_entities, idle_event, dispatch)
                if self.engine.running and not self.updating:
                    # We don't need to run two updates at the same time
                    self.updating = True
                    # print("Updating entities")
                    self.update_entities(self.time_step * idle_event.time_scale, dispatch, idle_event.scene)
                    # print("Finished Updating")
                    self.updating = False

