import sys
import traceback
from concurrent import futures
import time
from collections import deque, defaultdict
from contextlib import ExitStack
from itertools import chain
from typing import List, Type, DefaultDict, Union, Callable, Any, Deque, Dict, Optional

import pyglet

from kge.audio.audio_manager import AudioManager, Audio
from kge.clocks.updater import Updater
from kge.core import events
from kge.core.entity import BaseEntity
from kge.core.event_dispatcher import EventDispatcher
from kge.core.eventlib import EventMixin
from kge.core.events import Event
from kge.core.entity_manager import EntityManagerService, EntityManager
from kge.core.service_provider import ServiceProvider
from kge.core.logger import LoggerMixin
from kge.core.scene import BaseScene
from kge.core.service import Service

from kge.core.system import System
from kge.graphics.renderer import Renderer, WindowService
from kge.inputs.input_manager import InputManager, InputService
from kge.physics.fixed_updater import FixedUpdater
from kge.physics.physics_manager import PhysicsManager, Physics
from kge.resources.assetlib import AssetLoader

import asyncio

from kge.resources.events import AssetLoaded

_ellipsis = type(...)


class Engine(LoggerMixin, EventMixin):
    """
    The engine
    in order to run the engine, you must enter in by a with statement.
    Example:
        >>> engine = Engine(...)
        >>> with engine:
        >>>     engine.run()
    """

    def __init__(self, first_scene: Type[BaseScene], *,
                 basic_systems=(
                         # todo
                         Updater,
                         PhysicsManager,
                         # todo
                         FixedUpdater,
                         EventDispatcher,
                         Renderer,
                         InputManager,
                         AssetLoader,
                         AudioManager,
                         EntityManager,
                 ),
                 basic_services=(
                         Physics, EntityManagerService, Audio, InputService,
                         WindowService,
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
        self._last_idle_time = None  # last time the engine did update

        # Window
        self.window_title = window_title

        # the current event queue for the frame, and the event queue for the next frame
        self._event_queue = deque()  # type: Deque[Event]
        self._next_event_queue = deque()  # type: Deque[Event]
        self.event_loop = pyglet.app  # CustomEventLoop(self.loop_once) #

        # if you want to register new events to the engine directly,
        # Add it with 'register' method
        # This array holds theses events
        self._event_extensions: DefaultDict[Union[Type, _ellipsis], List[Callable[[Any], None]]] = defaultdict(list)

        # Systems
        self._systems_classes = list(chain(basic_systems, systems))
        self.systems = []  # type: List[System]

        # This is exit stack : the order to exit out of systems
        self._exit_stack = ExitStack()

        # time scale : in order to change the speed of our systems
        self.time_scale = 1.0

        # locator
        self._services_classes = basic_services  # type: List[Type[Service]]
        # thread loop and Async Loop
        # self.thread_loop = threading.Thread(target=lambda: self.main_loop())
        self.async_loop = None  # type: Optional[asyncio.AbstractEventLoop]

        # Executor for multi threading
        self._executor = futures.ThreadPoolExecutor()  # type: futures.thread.ThreadPoolExecutor
        self._jobs = deque()

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

    def on_quit(self, ev, dispatch):
        self.dispatch(events.StopScene(), immediate=True)

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
            self.systems.append(system)
            self._exit_stack.enter_context(system)

            # removed !
            # Start the system thread
            # system.start()

        # Then provide services
        for service in self._services_classes:
            if service.system_class in kinds:
                ServiceProvider.provide(service=service(instance=kinds[service.system_class]))

    def init(self):
        """
        Initialize the engine

        :return:
        """
        self.running = True
        self._last_idle_time = time.monotonic()
        self.activate_scene({"scene_class": self.first_scene,
                             "kwargs": self.scene_kwargs})

    def activate_scene(self, next_scene: dict):
        """
        Activating a scene

        :param next_scene: should be a dict representing the next scene
        :return:

        Example of use :
            >>> engine.activate_scene({
            >>>     "scene_class" : Scene,
            >>>     "kwargs" : {...},
            >>> })
        """
        scene = next_scene["scene_class"]
        if scene is None:
            return
        args = next_scene.get("args", [])
        kwargs = next_scene.get("kwargs", {})
        scene = scene(*args, **kwargs)
        scene.engine = self
        self._scenes.append(scene)
        self.dispatch(events.SceneStarted(), immediate=True)

    def run(self):
        """
        Run the engine

        :return:
        """
        if not self.entered:
            with self:
                self.init()
                # pyglet.clock.schedule_interval(lambda dt: self.loop_once(), 1 / 10_000)
                # self.thread_loop.start()
                # self.event_loop.run()
                self.main_loop()
        else:
            self.init()
            # pyglet.clock.schedule_interval(lambda dt: self.loop_once(), 1 / 10_000)
            # self.thread_loop.start()
            # self.event_loop.run()
            self.main_loop()

        # while self.running:
        #     continue

    def main_loop(self):
        """
        The main loop
        """
        n = 0
        self._last_idle_time = time.monotonic()
        # while self.running:
        n += 1

        # CUSTOM EVENT LOOP TO PYGAME
        # pyglet.clock.tick()

        # self.logger.info(f"LOOPED {n} times")
        # for window in pyglet.app.windows:
        #     window.switch_to()
        #     window.dispatch_events()
        #     window.dispatch_event('on_draw')
        #     window.flip()

        pyglet.clock.schedule_interval(self.loop_once, 1 / 10_000)
        pyglet.clock.schedule_interval(self.flush_jobs, 1 / 10_000)
        pyglet.app.run()

        # Set the running state to False to stop small scripts for updating
        self.flush_events()
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
        # self._executor.shutdown()
        self.logger.info("Finished Processes.")

    def flush_jobs(self, dt):
        """
        Flush Finished Jobs in order to close engine more quickly
        """
        for future in futures.as_completed(self._jobs):
            self._jobs.remove(future)


    def loop_once(self, dt):
        """
        Loop once

        :return: None
        """
        if not self.entered:
            raise ValueError("Cannot run before things have started",
                             self.entered)

        if self.running:
            # Get time_delta
            now = time.monotonic()
            time_delta = now - self._last_idle_time
            self._last_idle_time = now

            # dispatch events (they are sorted in reverse order)
            self.dispatch(events.Idle(time_delta * self.time_scale), immediate=True)

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
            self._event_queue.append(event)
        else:
            self._next_event_queue.append(event)

    # @staticmethod
    # def run_func_in_async_mode(callback: Callable[[Any], None], *args):
    #     """
    #     Run callback in async mode
    #     """
    #     # Sleep in order to let other tasks get processed
    #     await asyncio.sleep(0.0001)
    #     # Launcb Callback with provided args
    #     callback(*args)

    def dispatch_events(self):
        """
        Dispatch events to subsystems and entities

        :return:
        """
        # Get the last event
        event = self._event_queue.popleft()
        scene = self.current_scene
        event.scene = scene
        event.time_scale = self.time_scale

        # launch registered event handlers in async Mode
        extensions = chain(self._event_extensions[type(event)], self._event_extensions[...])
        for callback in extensions:
            # tasks.append(self.async_loop.create_task(self.run_func_in_async_mode(callback, event)))
            self._jobs.append(self._executor.submit(callback, event))

        self._jobs.append(self._executor.submit(self.__fire_event__, event, self.dispatch))

        # dispatch events on subsystems
        for system in self.systems:
            # if event is AssetLoaded event, then run it in the main thread
            # FIXME : FIND A BETTER WAY TO IMPLEMENT THIS
            if isinstance(event, AssetLoaded):
                system.__fire_event__(event, self.dispatch)

            self._jobs.append(
                self._executor.submit(system.__fire_event__, event, self.dispatch)
            )

        # Required for if we dispatch with no current scene.
        # Should only happen when the last scene stops via event.
        # def fire_scene_event(event):
        if scene is not None:
            if event.onlyEntity is None:
                self._jobs.append(self._executor.submit(scene.__fire_event__, event, self.dispatch))

                if scene.main_camera is not None:
                    self._jobs.append(self._executor.submit(scene.main_camera.__fire_event__, event, self.dispatch))

        # if type(event) is events.SceneStopped:
        #     # If event is quit then wait until each system has finished
        #

    def on_time_dilation(self, ev: events.TimeDilation, dispatch: Callable[[Event], None]):
        """
        Change the time scale
        """
        self.time_scale = ev.new_time_scale

    def on_start_scene(self, event: events.StartScene, dispatch: Callable[[Event], None]):
        """
        Start a new scene. The current scene pauses.
        """
        self.pause_scene()
        self.start_scene(event.new_scene, event.kwargs)

    def on_stop_scene(self, event: events.StopScene, dispatch: Callable[[Event], None]):
        """
        Stop a running scene. If there's a scene on the stack, it resumes.
        """
        self.stop_scene()
        if self.current_scene is not None:
            dispatch(events.SceneContinued())
        else:
            dispatch(events.Quit())

    def on_replace_scene(self, event: events.ReplaceScene, dispatch):
        """
        Replace the running scene with a new one.
        """
        self.stop_scene()
        self.start_scene(event.new_scene, event.kwargs)

    def pause_scene(self):
        """
        Pause the current scene

        :return:
        """
        # Empty the event queue before changing scenes.
        self.flush_events()
        self.dispatch(events.ScenePaused())
        self.dispatch_events()

    def stop_scene(self):
        """
        Stop the current scene

        :return:
        """
        # Empty the event queue before changing scenes.
        self.flush_events()
        self.dispatch(events.SceneStopped(), immediate=True)
        # self.dispatch_events()
        if self._scenes:
            self._scenes.pop()

    def start_scene(self, scene: Union[Type[BaseScene], BaseScene], kwargs: Dict[str, Any]):
        """
        Start a scene

        :param scene:
        :param kwargs:
        :return:
        """
        self.running = True
        if isinstance(scene, type):
            scene = scene(**(kwargs or {}))

        # Set engine to self
        if scene.engine is None:
            scene.engine = self

        self._scenes.append(scene)
        self.dispatch(events.SceneStarted(), immediate=True)

    def register(self, event_type: Union[Type[Event], _ellipsis], callback: Callable[[Event], None]):
        """
        Register a callback to be applied to an event at time of dispatching.

        Primarily to be used by subsystems.

        The callback will receive the event. Your code should modify the event
        in place. It does not need to return it.

        :param event_type: The class of an event.
        :param callback: A callable, must accept an event, and return no value.
        :return: None
        """
        if not isinstance(event_type, type) and event_type is not ...:
            raise TypeError(f"{type(self)}.register requires event_type to be a type.")
        if not callable(callback):
            raise TypeError(f"{type(self)}.register requires callback to be callable.")
        self._event_extensions[event_type].append(callback)

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
