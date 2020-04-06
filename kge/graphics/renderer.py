import logging
import time
from typing import Union, List, Sequence

import pyglet
from math import ceil
from pyglet.gl import *

import kge
from kge.core import events
from kge.core.component_system import ComponentSystem
from kge.core.constants import DEFAULT_RESOLUTION, IS_FULLSCREEN, IS_RESIZABLE, DEFAULT_FPS, BLACK, \
    MAX_LAYERS
from kge.core.service import Service
from kge.graphics.render_component import RenderComponent
from kge.utils.dotted_dict import DottedDict
from kge.utils.vector import Vector


class Square:
    """
    FIXME : REMOVE THIS (?)
    """

    def __init__(self, color: Sequence[int]):
        self.color = (color[0], color[1], color[2], color[3])

        self.vertices = [
            Vector(-1 / 2, 1 / 2),
            Vector(1 / 2, 1 / 2),
            Vector(1 / 2, -1 / 2),
            Vector(-1 / 2, -1 / 2),
        ]

        self.mode = GL_QUADS
        self.num_points = 4


class OutLinedSquare:
    """
    FIXME : REMOVE THIS (?)
    """

    def __init__(self, color: Sequence[int]):
        self.color = (color[0], color[1], color[2], color[3])

        self.vertices = [
            # Horizontal
            Vector(-1 / 2, 1 / 2),
            Vector(1 / 2, 1 / 2),
            Vector(1 / 2, -1 / 2),
            Vector(-1 / 2, -1 / 2),
            # Vertical
            Vector(-1 / 2, -1 / 2),
            Vector(-1 / 2, 1 / 2),
            Vector(1 / 2, 1 / 2),
            Vector(1 / 2, -1 / 2),
        ]
        self.mode = GL_LINES
        self.num_points = 8


class Renderer(ComponentSystem):
    """
    The system which task is to render all elements in a scene
    TODO:
        - Set FullScreen by script
        - Resize by script
        - Make this system generic for all kinds of graphic elements
    """

    def __init__(self, resolution=DEFAULT_RESOLUTION, fullscreen=IS_FULLSCREEN, resizable=IS_RESIZABLE, vsync=True,
                 **_):
        super().__init__(**_)
        self.components_supported = [RenderComponent]
        self.accumulated_time = 0
        self.last_tick = None
        self.start_time = None
        self.time_step = 1 / DEFAULT_FPS
        self.window = None  # type: Union[pyglet.window.Window, None]
        self._vsync = vsync

        # TODO : THESE ATTRIBUTES DO NOT WORK PROPERLY
        self._is_fullscreen = fullscreen
        self._is_resizable = resizable
        self.resolution = resolution

        self.window_size = Vector.Zero()

        # Scene Variables
        self._bgc = tuple(unit / 255 for unit in BLACK[:3])

        # batch
        self.batch = None  # type: Union[pyglet.graphics.Batch, None]
        self.grid_batch = None  # type: Union[pyglet.graphics.Batch, None]

        # FPS COUNTER
        self.fps_display = None  # type: Union[pyglet.window.FPSDisplay, pyglet.text.Label, None]

        # layers
        self.layers = [pyglet.graphics.OrderedGroup(i) for i in range(MAX_LAYERS)]
        # self.window_size = Vector.Zero()
        self.to_draw = []  # Vertices to draw

        # Frame calculations
        self.fps = 0
        self.last_step = time.monotonic()

    def on_disable_entity(self, event: events.DisableEntity, dispatch):
        if hasattr(event.entity, "renderer"):
            event.entity.renderer.__fire_event__(event, dispatch)

    def on_enable_entity(self, event: events.EnableEntity, dispatch):
        if hasattr(event.entity, "renderer"):
            event.entity.renderer.__fire_event__(event, dispatch)

    def on_destroy_entity(self, event: events.DestroyEntity, dispatch):
        super(Renderer, self).on_destroy_entity(event, dispatch)
        if hasattr(event.entity, "renderer"):
            event.entity.renderer.__fire_event__(event, dispatch)

    def on_scene_stopped(self, event: events.SceneStopped, dispatch):
        """
        When scene get stopped, remove all render components & dispatch event
        """
        for renderer in self.event_map[type(event).__name__]:
            renderer.__fire_event__(event, dispatch)

        # clear components & remake the batch
        self.batch = pyglet.graphics.Batch()
        self.window_size = Vector.Zero()
        super(Renderer, self).on_scene_stopped(event, dispatch)

    def __enter__(self):
        self.window = pyglet.window.Window(
            vsync=self._vsync,
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
        # self.window.on_resize = lambda w, h: self.resize_viewport(w, h)

        # Keeping the resolution
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # Enable Alpha transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Schedule render update to the time step
        pyglet.clock.schedule(self.render)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.engine.event_loop.has_exit = True

    def on_quit(self, ev: events.Quit, dispatch):
        if self.engine is not None:
            self.engine.event_loop.has_exit = True

    def close(self):
        self._dispatch(events.Quit(), immediate=True)
        self.window.close()
        return pyglet.event.EVENT_HANDLED

    def display_grid(self):
        """
        FIXME : ONLY FOR DEV PURPOSES
        """
        hash = self.engine.current_scene.spatial_hash
        camera = self.engine.current_scene.main_camera

        # cell size
        size = self.engine.current_scene.spatial_hash.cell_size
        # size_pixels = camera.unit_to_pixels(self.engine.current_scene.spatial_hash.cell_size) # type: float

        # Frame width & height
        fw, fh = camera.frame_width, camera.frame_height

        # number of columns & Lines
        nb_cols = int(ceil(fw / size))
        nb_lines = int(ceil(fh / size))

        # the beginning positions
        depX, depY = camera.frame_left + size / 2, camera.real_frame_bottom + size / 2
        posY = depY

        for i in range(nb_lines):
            posX = depX
            for j in range(nb_cols):
                curPos = Vector(posX, posY)
                # find if cells is not empty
                in_cells = hash.search(curPos, Vector.Unit() * (size / 4))

                # if cell is not empty, then draw a filled square else, draw a hollow square
                shape2 = None
                if in_cells:
                    shape2 = Square((0, 0, 255, 50))

                shape = OutLinedSquare((0, 255, 0, 255))

                vertices = []

                # calculate new vertices for the grid
                for v in shape.vertices:
                    vertices.extend(
                        tuple(camera.world_to_screen_point(
                            curPos + v * size
                        ))
                    )

                self.grid_batch.add(
                    shape.num_points, shape.mode, pyglet.graphics.OrderedGroup(25),
                    ("v2d/stream", tuple(vertices)),
                    ("c4Bn/dynamic",
                     shape.color * shape.num_points)
                )

                if shape2 is not None:
                    vertices = []
                    # calculate new vertices for the grid
                    for v in shape2.vertices:
                        vertices.extend(
                            tuple(camera.world_to_screen_point(
                                curPos + v * size
                            ))
                        )

                    self.grid_batch.add(
                        shape2.num_points, shape2.mode, pyglet.graphics.OrderedGroup(24),
                        ("v2d/stream", tuple(vertices)),
                        ("c4Bn/dynamic",
                         shape2.color * shape2.num_points)
                    )

                posX += size
            posY += size

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

        # Draw physics data
        if self.logger.getEffectiveLevel() == logging.DEBUG:
            physX = kge.ServiceProvider.getPhysics()
            physX.debug_drawer.batch.draw()

        # display Grid
        if self.engine.current_scene.show_grid == True:
            # print(self.grid_batch.group_map)
            self.grid_batch.draw()

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

            scene = self.engine.current_scene


            for entity in scene.entity_layers():  # type: Union[kge.Sprite]
                # Render only sprites
                element = entity.renderer.render(scene)
                if element is not None:
                    self.to_draw.append(element)

            # FIXME : ONLY FOR DEV PURPOSES
            if self.engine.current_scene.show_grid:
                self.grid_batch = pyglet.graphics.Batch()
                self.display_grid()

            new_win_size = Vector(self.window.width, self.window.height)
            if self.window_size != new_win_size:
                self.window_size = new_win_size
                self.engine.current_scene.main_camera.resolution = new_win_size
                self._dispatch(events.WindowResized(new_size=self.window_size))


class WindowService(Service):
    system_class = Renderer
    _system_instance: Renderer

    @property
    def window(self) -> pyglet.window.Window:
        return self._system_instance.window

    # FIXME : FULLSCREEN NOT WORKING PROPERLY
    @property
    def fullscreen(self) -> bool:
        return self._system_instance.window.fullscreen

    @fullscreen.setter
    def fullscreen(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Fullscreen should be a bool")
        self._system_instance.window.set_fullscreen(value)

    @property
    def batch(self) -> pyglet.graphics.Batch:
        return self._system_instance.batch

    @property
    def render_layers(self) -> List[pyglet.graphics.OrderedGroup]:
        return self._system_instance.layers
