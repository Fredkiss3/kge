import sys
import traceback
from concurrent import futures
from collections import deque
from contextlib import ExitStack
from itertools import chain
from typing import List, Type, Union, Callable, Any, Deque, Dict

import pyglet
from kge.audio.audio_manager import AudioManager, Audio
from kge.clocks.updater import Updater
from kge.core import events
from kge.core.behavior_manager import BehaviourManager
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
from kge.physics.physics_manager import PhysicsManager, Physics, DebugDrawService
from kge.resources.assetlib import AssetLoader

from kge.resources.events import AssetLoaded

_ellipsis = type(...)


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
                         Updater,
                         PhysicsManager,
                         FixedUpdater,
                         EventDispatcher,
                         Renderer,
                         InputManager,
                         AssetLoader,
                         AudioManager,
                         EntityManager,
                         BehaviourManager,
                 ),
                 basic_services=(
                         Physics, EntityManagerService, Audio, InputService,
                         WindowService, DebugDrawService,
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

        # This is exit stack : the order to exit out of systems
        self._exit_stack = ExitStack()

        # time scale : in order to change the speed of our systems
        self.time_scale = 1.0

        # for services
        self._services_classes = basic_services  # type: List[Type[Service]]

        # Executor for multi threading
        self._executor = futures.ThreadPoolExecutor()
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
            # appends system to independent threads
            if not isinstance(system, (Updater, FixedUpdater, AssetLoader, AudioManager, EntityManager)):
                self.systems.append(system)

            self._exit_stack.enter_context(system)

        # Then provide services
        for service in self._services_classes:
            if service.system_class in kinds:
                ServiceProvider.provide(service=service(
                    instance=kinds[service.system_class]))

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
        BaseScene.engine = self
        scene = scene(*args, **kwargs)
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
                self.main_loop()
        else:
            self.init()
            self.main_loop()

    def main_loop(self):
        """
        The main loop
        """
        pyglet.clock.schedule_interval(self.loop_once, 1 / 10_000)
        # Flush the jobs created
        pyglet.clock.schedule_interval(self.flush_jobs, 1 / 10)
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
        self._executor.shutdown()
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

        # launch registered event handlers
        if self.has_event(event):
            self._jobs.append(self._executor.submit(
                self.__fire_event__, event, self.dispatch))

        # dispatch events on subsystems
        for system in self.systems:
            # FIXME : FIND A BETTER WAY TO IMPLEMENT THIS -> By Regrouping the sprite renderers on renderer system
            # if event is AssetLoaded event, then run it in the main thread
            if isinstance(event, AssetLoaded):
                # Only dispatch this event to EventDispatcher on main thread
                if isinstance(system, EventDispatcher):
                    system.__fire_event__(event, self.dispatch)
                continue
            elif isinstance(event, events.DebugDraw) and isinstance(system, (PhysicsManager, BehaviourManager, EventDispatcher)):
                system.__fire_event__(event, self.dispatch)
                continue
            elif isinstance(event, (events.Update, events.FixedUpdate, events.LateUpdate)):
                # Only to Behaviours
                if isinstance(system, BehaviourManager):
                    self._jobs.append(
                        self._executor.submit(
                            system.__fire_event__, event, self.dispatch)
                    )

                # Dispatch this event to event dispatcher
                if isinstance(event, (events.LateUpdate)) and isinstance(system, EventDispatcher):
                    self._jobs.append(
                        self._executor.submit(
                            system.__fire_event__, event, self.dispatch)
                    )
                continue
            else:
                self._jobs.append(
                    self._executor.submit(
                        system.__fire_event__, event, self.dispatch)
                )
            # TODO
            # if isinstance(system, Renderer):
            #     system.__fire_event__(event, self.dispatch)
            #     continue

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
        self.dispatch_events()
        print("Dispatch")
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
