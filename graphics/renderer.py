import threading
import time
from typing import Union, List, Callable

import pyglet
from pyglet.gl import *
import kge
from kge.utils.dotted_dict import DottedDict
from kge.utils.vector import Vector
from kge.core import events
from kge.core.constants import DEFAULT_RESOLUTION, WINDOW_POSITION, IS_FULLSCREEN, IS_RESIZABLE, DEFAULT_FPS, BLACK, \
    RED, BLUE
from kge.core.service import Service
from kge.core.system import System
from kge.graphics.sprite_renderer import SpriteRenderer
import logging


class Renderer(System):
    """
    The system which task is to render all elements in a scene
    TODO:
        - Set FullScreen by script
        - Resize by script
        - Make this system generic for all kinds of graphic elements
    """

    def __init__(self, resolution=DEFAULT_RESOLUTION, fullscreen=IS_FULLSCREEN, resizable=IS_RESIZABLE, **_):
        super().__init__(**_)
        self.accumulated_time = 0
        self.last_tick = None
        self.start_time = None
        self.time_step = 1 / DEFAULT_FPS
        self.window = None  # type: Union[pyglet.window.Window, None]

        self._is_fullscreen = fullscreen
        self._is_resizable = resizable
        self.resolution = resolution

        # Scene Variables
        self._camera_zoom = 0
        self._bgc = tuple(unit / 255 for unit in BLACK[:3])

        # batch
        self.batch = None  # type: Union[pyglet.graphics.Batch, None]

        # FPS COUNTER
        self.fps_display = None  # type: Union[pyglet.window.FPSDisplay, pyglet.text.Label, None]

        # layers
        self.layers = [pyglet.graphics.OrderedGroup(i) for i in range(20)]
        self.window_size = Vector.Zero()
        self.to_draw = []  # Vertices to draw

        # Frame calculations
        self.fps = 0
        self.last_step = time.monotonic()

    def __enter__(self):
        self.window = pyglet.window.Window(
            # todo: allow vsync or not ?
            vsync=False,
            width=self.resolution[0],
            height=self.resolution[1],
            resizable=self._is_resizable,
            fullscreen=self._is_fullscreen,
            caption=f"{self.engine.window_title}"
        )

        # Batch for drawing
        # self.fps_display = pyglet.window.FPSDisplay(window=self.window)
        self.fps_display = pyglet.text.Label(x=10, y=10,
                                             font_size=24, bold=True,
                                             color=(127, 127, 127, 200))
        self.batch = pyglet.graphics.Batch()

        # Window events
        self.window.on_draw = lambda: self.draw()
        self.window.on_close = lambda: self.close()

        # Keeping the resolution
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # Enable Alpha transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Schedule render update to the time step
        pyglet.clock.schedule(self.render)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.engine.event_loop.has_exit = True

    def close(self):
        self._dispatch(events.Quit(), immediate=True)
        self.window.close()
        return pyglet.event.EVENT_HANDLED

    def draw(self):
        """
        Draw the window
        """
        now = time.monotonic()
        if now - self.last_step >= 1:
            self.fps_display.text = f"{self.fps} FPS"
            self.last_step = time.monotonic()
            self.fps = 0
        self.fps += 1

        # Clear the screen
        self.window.clear()
        glClearColor(*self._bgc, 1)

        self.batch.draw()

        if self.to_draw:
            for shape, mode in self.to_draw:
                shape.draw(mode)

        # Display FPS
        if self.engine.current_scene.display_fps == True:
            self.fps_display.draw()

        return pyglet.event.EVENT_HANDLED

    def render(self, dt: float):
        """
        Render calculations
        """
        scene = self.engine.current_scene
        if scene is not None:
            # set scene color
            self._bgc = tuple(
                unit / 255 for unit in scene.background_color[:3]
            )

            self.to_draw = []

            elist = list(scene.entity_layers())

            for entity in elist:  # type: Union[kge.Sprite]
                # Render only sprites
                element = entity.sprite_renderer.render(scene)
                if element is not None:
                    self.to_draw.append(element)

            new_win_size = Vector(self.window.width, self.window.height)
            if self.window_size != new_win_size:
                self.window_size = new_win_size
                self.engine.current_scene.main_camera.resolution = DottedDict(width=new_win_size.x,
                                                                              height=new_win_size.y)
                self._dispatch(events.WindowResized(self.window_size))


class WindowService(Service):
    system_class = Renderer
    _system_instance: Renderer

    @property
    def window(self) -> pyglet.window.Window:
        return self._system_instance.window

    @property
    def batch(self) -> pyglet.graphics.Batch:
        return self._system_instance.batch

    @property
    def render_layers(self) -> List[pyglet.graphics.OrderedGroup]:
        return self._system_instance.layers
