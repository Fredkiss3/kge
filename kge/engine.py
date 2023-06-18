import random
import sys
import time
import traceback
from collections import deque
from concurrent import futures
from contextlib import ExitStack
from itertools import chain
from typing import List, Type, Union, Callable, Any, Deque, Dict, Tuple

import pyglet

from kge.audio.audio_manager import AudioManager, Audio
from kge.clocks.updater import Updater
from kge.core import events
from kge.core.behavior_manager import BehaviourManager
from kge.core.entity import BaseEntity
from kge.core.entity_manager import EntityManagerService, EntityManager
from kge.core.event_dispatcher import EventDispatcher
from kge.core.eventlib import EventMixin
from kge.core.events import Event
from kge.core.logger import LoggerMixin
from kge.core.scene import BaseScene
from kge.core.service import Service
from kge.core.service_provider import ServiceProvider
from kge.core.system import System
from kge.graphics.anim_system import AnimSystem
from kge.graphics.renderer import Renderer, Window
from kge.inputs.input_manager import InputManager, Inputs
from kge.physics.physics_manager import PhysicsManager, Physics, DebugDraw
from kge.resources.assetlib import AssetLoader


# from kge.ui.ui_manager import UIManager

def snake_to_camel(meth_name: str):
    if not meth_name.startswith("on_") or (meth_name[-1] not in "azertyuiopqsdfghjklmwxcvbn"):
        return None
    else:
        event_name = meth_name[3:].split("_")
        event = ""
        for name in event_name:  # type: str
            if len(name.strip()) > 0:
                event += name.capitalize()
        return event


class Engine(LoggerMixin, EventMixin):
    """
    The engine is the boss, the class that launches every system
    in order to run the engine, you must enter in by a with statement.
    Example:
        >>> engine = Engine(...)
        >>> with engine:
        >>>     engine.run()
    """

    def __init__(self, first_scene: Type[BaseScene], *,
                 basic_systems=(
                         # Periodic Systems
                         Renderer,
                         Updater,

                         # Contextual Systems
                         AnimSystem,
                         # AudioManager,
                         BehaviourManager,
                         EntityManager,
                         EventDispatcher,
                         InputManager,
                         PhysicsManager,
                         # UIManager,
                 ),
                 basic_services=(
                         # Inner Services
                         EntityManagerService,

                         # Services provided to users
                         # Audio,
                         Inputs,
                         Physics,
                         Window,
                         DebugDraw,
                 ),
                 systems=(), scene_kwargs=None, window_title: str = None, **kwargs):
        super(Engine, self).__init__()

        # The engine configuration
        self.first_scene = first_scene
        self.scene_kwargs = scene_kwargs or {}
        self.kwargs = kwargs

        # The engine state
        self._scenes = []  # type: List[BaseScene]
        self.running = False
        self.entered = False

        # Window
        self.window_title = window_title

        # the current event queue for the frame, and the event queue for the next frame
        self._event_queue = deque()  # type: Deque[Event]
        self._next_event_queue = deque()  # type: Deque[Event]
        self.event_loop = pyglet.app

        # Systems
        self._systems_classes = list(chain(basic_systems, systems))
        self.systems = []  # type: List[System]
        self.wildcards_systems = []  # type: List[System]

        # This is exit stack : the order to exit out of systems
        self._exit_stack = ExitStack()

        # time scale : in order to change the speed of our systems
        self.time_scale = 1.0

        # for services
        self._services_classes = basic_services  # type: List[Type[Service]]

        # Executor for multi threading
        self._executor = futures.ThreadPoolExecutor()
        self._jobs = deque()

        # Time deltas for update, fixed_update & render
        self.update_dt, self.fixed_dt, self.render_dt, = 1, 1, 1
        self.event_map = dict()  # type: Dict[str, List[EventMixin]]

        # Register events for engine
        self.register_events(self)

    def register_events(self, b: EventMixin):
        """
        Map names of events to event mixins which need to handle the event
        """
        for attribute in dir(b):
            if attribute.startswith("on_") and callable(getattr(b, attribute)):
                name = snake_to_camel(attribute)
                try:
                    l = self.event_map[name]
                except KeyError:
                    self.event_map[name] = [b]
                else:
                    l.append(b)

    def unregister_events(self, b: EventMixin):
        """
        Remove the component from event map
        """
        k_l = dict()
        for k, v in self.event_map.items():
            if b in v:
                v.remove(b)
                k_l[k] = v

        # Remove event from Map if there is no more entity for it
        for k, v in k_l.items():
            if len(v) == 0:
                self.event_map.pop(k)
        k_l.clear()

    def append_job(self, func: Callable, *args, **kwargs):
        """
        Append a job to this engine
        """
        self._jobs.append(
            self._executor.submit(
                func, *args, **kwargs
            )
        )

    @property
    def current_scene(self):
        """
        Get the current scene

        :return:
        """
        try:
            return self._scenes[-1]
        except IndexError:
            return None

    def __enter__(self):
        self.logger.info("Entering context")
        self.start_systems()
        self.entered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info("Exiting context")
        self.running = False
        self.entered = False
        self._exit_stack.close()

    def start_systems(self):
        """
        Start the systems

        :return:
        """
        if self.systems:
            return

        kinds = {}
        # Add the system classes in systems
        for system in self._systems_classes:
            if isinstance(system, type):
                t = system
                system = system(engine=self, **self.kwargs)  # type: System
                kinds[t] = system
            # appends systems
            if not isinstance(system, (AssetLoader, AudioManager)):
                self.systems.append(system)

            if isinstance(system, (EventDispatcher, BehaviourManager)):
                self.wildcards_systems.append(system)
            else:
                # Register events for the systems
                self.register_events(system)

            self._exit_stack.enter_context(system)

        # Then provide services
        for service in self._services_classes:
            if service.system_class in kinds:
                ServiceProvider.provide(service=service, system=kinds[service.system_class])

    def init(self):
        """
        Initialize the engine

        :return:
        """
        self.running = True
        self.activate_scene({"scene_class": self.first_scene,
                             "kwargs": self.scene_kwargs})

    def activate_scene(self, next_scene: dict):
        """
        Activating a scene at the beginning of the engine

        :param next_scene: should be a dict representing the next scene

        Example of use :
            >>> engine.activate_scene({
            >>>     "scene_class" : Scene,
            >>>     "kwargs" : {...},
            >>> })
        """
        scene = next_scene["scene_class"]
        if scene is None:
            return

        kwargs = next_scene.get("kwargs", {})
        args = next_scene.get("args", ())
        self.start_scene(scene, args, kwargs)

    def run(self):
        """
        Run the engine
        """
        if not self.entered:
            with self:
                self.init()
                self.main_loop()
        else:
            self.init()
            self.main_loop()

    def main_loop(self):
        """
        The main loop
        """
        pyglet.clock.schedule(self.loop_once)
        # Flush the jobs created
        self.event_loop.run()

        # Set the running state to False to stop small scripts for updating
        self.flush_events()
        self.dispatch(events.SceneStopped(), immediate=True)
        self.dispatch(events.Quit(), immediate=True)
        self.loop_once()
        self.running = False

        for future in futures.as_completed(self._jobs):
            try:
                data = future.result()
            except Exception as e:
                self.logger.error(f'A fatal error Happened : {e}')
                traceback.print_exc(file=sys.stdout)
                self._executor.shutdown(wait=False)
            else:
                pass
        self._executor.shutdown()
        self.logger.info("Finished Processes.")

    def loop_once(self, dt=None):
        """
        Loop once
        """
        if not self.entered:
            raise ValueError("Cannot run before things have started",
                             self.entered)

        if self.running:
            # get last events added to the queue
            self._event_queue.extend(self._next_event_queue)
            self._next_event_queue = deque()

            while self._event_queue:
                self.dispatch_events()

    def on_entity_destroyed(self, ev: events.EntityDestroyed, dispatch: Callable[[Event], None]):
        """
        Remove an entity from the scene
        """
        self.current_scene.remove(ev.entity)

    def on_destroy_entity(self, ev: events.DestroyEntity, dispatch: Callable[[Event], None]):
        """
        Destroy an entity
        """
        ev.entity.is_active = False
        ev.scene.remove(ev.entity)

        # dispatch the event
        self.dispatch(events.EntityDestroyed(
            entity=ev.entity
        ), immediate=True)

    def dispatch(self, event: Event, immediate: bool = False):
        """
        Add an event to the event queue.
        If the 'immediate' parameter is set to true, it will be added
        to the current frame event queue, if not, then it will be added
        to the next frame.

        Thread-safe.
        """
        event.scene = self.current_scene
        event.time_scale = self.time_scale

        if immediate:
            self._event_queue.appendleft(event)
        else:
            self._next_event_queue.append(event)

    def dispatch_events(self, on_main=False):
        """
        Dispatch events to subsystems and entities

        :return:
        """
        # This is to fix bugs when using random
        random.seed(time.monotonic())

        # Get the last event
        event = self._event_queue.popleft()
        scene = self.current_scene
        event.scene = scene
        event.time_scale = self.time_scale

        if on_main:
            # If action should be on main then run it for everyone
            for system in self.systems:
                system.__fire_event__(event, self.dispatch)
        else:
            receivers = self.event_map.get(type(event).__name__, [])
            for system in receivers:
                system.__fire_event__(event, self.dispatch)

            for system in self.wildcards_systems:
                system.__fire_event__(event, self.dispatch)

    def on_time_dilation(self, ev: events.TimeDilation, dispatch: Callable[[Event], None]):
        """
        Change the time scale
        """
        self.time_scale = ev.new_time_scale

    def on_stop_scene(self, event: events.StopScene, dispatch: Callable[[Event], None]):
        """
        Stop a running scene. If there's a scene on the stack, it resumes.
        """
        self.stop_scene()
        if self.current_scene is not None:
            dispatch(events.SceneContinued())

    def on_replace_scene(self, event: events.ReplaceScene, dispatch):
        """
        Replace the running scene with a new one.
        """
        self.stop_scene()
        self.start_scene(event.new_scene, event.args, event.kwargs)

    def pause_scene(self):
        """
        Pause the current scene
        """
        # Empty the event queue before changing scenes.
        self.flush_events()
        self.dispatch(events.ScenePaused())
        self.dispatch_events()

    def stop_scene(self):
        """
        Stop the current scene
        """
        # Empty the event queue before changing scenes.
        self.flush_events()
        self.dispatch(events.SceneStopped(), immediate=True)
        self.dispatch_events(on_main=True)

        if self._scenes:
            self._scenes.pop()

    def __repr__(self):
        return f"{type(self).__name__}(Kiss Game Engine)"

    def start_scene(self, scene: Union[Type[BaseScene], BaseScene], args: Tuple, kwargs: Dict[str, Any]):
        """
        Start a new scene
        """
        self.dispatch(events.StartScene(), immediate=True)
        self.dispatch_events(on_main=True)

        self.running = True
        if isinstance(scene, type):
            scene = scene(*(args or ()), **(kwargs or {}))

        # Set engine to self
        if scene.engine is None:
            scene.engine = self

        self._scenes.append(scene)
        # setup the scene, then dispatch scene started event
        scene.__fire_event__(events.SetupScene(scene=scene), self.dispatch)

        self.dispatch(events.SceneStarted(), immediate=True)

    def flush_events(self):
        """
        Flush the event queue.

        Call before doing anything that will cause signals to be delivered to
        the wrong scene.
        """
        self._event_queue = deque()
        self._next_event_queue = deque()


if __name__ == '__main__':
    from kge import Scene
    import logging

    logging.basicConfig(level=logging.DEBUG)


    class Sprite(BaseEntity):

        def on_update(self, time_delta: float, dispatch: Callable[[Event], None]):
            print("Update Entity")

        def on_init(self, init_event: events.Init, dispatch):
            print("Initialization")


    def setup(scene: Scene):
        player = Sprite(name="player")
        scene.add(player)


    engine = Engine(Scene, scene_kwargs={
        "set_up": setup
    })

    print(engine._systems_classes)

    with engine:
        engine.run()

    pass
