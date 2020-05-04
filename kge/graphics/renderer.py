import io
import logging
import sys
import time
from typing import Union, List, Optional, Tuple

import imgui
import pyglet
from imgui.integrations.pyglet import PygletRenderer
from pyglet.gl import *

import kge
from kge.core import events
from kge.core.component_system import ComponentSystem
from kge.core.constants import DEFAULT_RESOLUTION, IS_FULLSCREEN, IS_RESIZABLE, DEFAULT_FPS, BLACK, \
    MAX_LAYERS, RED, WHITE, YELLOW
from kge.core.service import Service
from kge.graphics.render_component import RenderComponent
from kge.utils.color import Color
from kge.utils.vector import Vector


class DebugConsole(object):
    """
    Console Used For DEBUG, it aims to wraps IMGUI calls
    """
    input: str = ""
    items: List[Tuple[str, Color]] = []
    output_stream: io.StringIO = io.StringIO()
    scroll_down: bool = False

    def add_log(self, log: str):
        self.items.append((log, YELLOW))

    def add_error(self, error):
        self.items.append((error, RED))

    def add_output(self, output: str):
        self.items.append((output, WHITE))

    def render(self, fps: str):
        # Imgui Renderer
        imgui.new_frame()

        imgui.begin("Debug Console", False, imgui.WINDOW_NO_FOCUS_ON_APPEARING)

        # Show Everything
        self._show_fps(fps)
        self._show_input_line()
        self._show_text_output()

        imgui.end()

        # Render Imgui
        imgui.render()

    def _show_input_line(self):
        # [SECTION] INPUT LINE
        imgui.begin_child(
            "INPUT LINE", height=40, border=True)

        # CLear Button
        if imgui.button('CLEAR', height=20, width=50):
            self.items.clear()

        # Set Same Line
        imgui.same_line()

        # Scroll Bottom Button
        self.scroll_down = imgui.button('BOTTOM', height=20, width=50)

        # Set Same Line
        imgui.same_line()

        # Show Filter TextField
        changed, self.input = imgui.input_text(
            'Filter',
            self.input,
            256
        )

        imgui.end_child()

    def _show_text_output(self):
        # [SECTION] LINE
        imgui.begin_child(
            "TEXT OUTPUT", border=True,
            flags=imgui.WINDOW_HORIZONTAL_SCROLLING_BAR)

        items = filter(lambda i: self.input.lower() in i[0].lower(), self.items)
        for item, color in items:
            # if self.input.lower() in item.lower():
            imgui.text_colored(item, *[c / 255 for c in color])

        if self.scroll_down or imgui.get_scroll_y() >= imgui.get_scroll_max_y():
            imgui.set_scroll_here(1.0)

        imgui.end_child()

    def _show_fps(self, fps: str):
        # [SECTION] FPS
        imgui.begin_child(
            "FPS", height=30, border=True, )

        imgui.text(f"GAME FPS : {fps}")
        imgui.end_child()


class LoadingFeedBack(object):
    def __init__(self):
        self.loaded = False

        # The loading Label
        self.loading_label = None  # type: Optional[pyglet.text.Label]

        # Our Brand
        self.brand = None  # type: Optional[pyglet.text.Label]

        # Entered ?
        self.entered = False

    @property
    def text(self):
        return '' if self.loading_label is None else self.loading_label.text

    @text.setter
    def text(self, val: str):
        if self.loading_label is not None:
            self.loading_label.text = f"{val}"

    def __enter__(self):
        # The loading Label
        self.loading_label = pyglet.text.Label(
            'PREPARING ENTITIES...', font_size=10, bold=True,
            x=40,
            y=20,
        )

        # Our Brand
        self.brand = pyglet.text.Label(
            'KISS GAME ENGINE', font_size=20, bold=True,
            x=40,
            y=40,
        )

        self.entered = True

    def __exit__(self, *_, **__):
        pass

    def draw(self, window: "pyglet.window.Window"):
        if self.loading_label is not None and self.brand is not None:
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glPushMatrix()
            gl.glLoadIdentity()

            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glPushMatrix()
            gl.glLoadIdentity()
            gl.glOrtho(0, window.width, 0, window.height, -1, 1)

            self.loading_label.draw()
            self.brand.draw()

            gl.glPopMatrix()

            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glPopMatrix()

    def delete(self):
        self.loading_label.delete()
        self.brand.delete()
        self.loading_label = None
        self.brand = None


class Renderer(ComponentSystem):
    """
    The system which task is to render all elements in a scene
    TODO:
        - Set Pixel Ratio Dynamically
        - Set FullScreen by script
        - Resize Window by script
        - LOOK FOR 'pyglet Z ordering with Sprite' -> For Applying 'Order in layer' (?)
        - Camera Jittering :
            -> glScalef not synced with camera position ?
    """

    def __init__(self,
                 resolution=DEFAULT_RESOLUTION,
                 show_console=False,
                 console_output: io.StringIO = io.StringIO(),
                 fullscreen=IS_FULLSCREEN, resizable=IS_RESIZABLE, vsync=False,
                 **_):
        super().__init__(**_)

        # Show Debug Console
        self.display_console = show_console

        # String IO for console debugging
        self.log_output = console_output
        self.err_output = io.StringIO()
        self.output = io.StringIO()

        # Debug Console
        self._console = DebugConsole()

        # To Draw
        self.to_draw = []

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
        self.batch = None  # type: Optional[pyglet.graphics.Batch]
        self.grid_batch = None  # type: Optional[pyglet.graphics.Batch]

        # layers
        self.layers = [pyglet.graphics.OrderedGroup(i) for i in range(MAX_LAYERS)]

        # Frame calculations
        self.fps = 0
        self.FPS = 0
        self.last_step = time.monotonic()

        # imgui implementation
        self.imgui_impl = None  # type: Optional[PygletRenderer]

        # TODO : UI Batch (?)
        self.ui_batch = pyglet.graphics.Batch()

        # Loading FeedBack
        self._load_feedback = None  # type: Optional[LoadingFeedBack]

    def on_window_resized(self, event: events.WindowResized, dispatch):
        """
        FIXME : CHANGE THIS
        :param event:
        :param dispatch:
        :return:
        """
        # scene = self.engine.current_scene
        # if scene is not None:
        #     for canvas in scene.entity_layers(kge.Canvas, renderable=False):  # type: kge.Canvas
        #         canvas.renderer.delete()
        #         canvas.dirty = True
        pass

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
        with LoadingFeedBack() as l:
            self._load_feedback = l

        self.window_size = Vector.Zero()

        # keep camera zoom
        self._zoom = 1

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

        # show console ?
        if self.display_console:
            sys.stdout = self.output
            sys.stderr = self.err_output

        # Minimum size only if resizable
        if self._is_resizable:
            self.window.set_minimum_size(200, 200)

        # Batch for drawing
        self.batch = pyglet.graphics.Batch()

        # Window events
        self.window.on_draw = lambda: self.draw()
        self.window.on_close = lambda: self.close()

        # Enable Alpha transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # create imgui context
        imgui.create_context()
        self.imgui_impl = PygletRenderer(self.window)

        # Loading FeedBack
        with LoadingFeedBack() as l:
            self._load_feedback = l

        # Schedule render update to the time step
        pyglet.clock.schedule(self.render)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.engine.event_loop.has_exit = True
        self.imgui_impl.shutdown()

    def on_quit(self, ev: events.Quit, dispatch):
        if self.engine is not None:
            self.engine.event_loop.has_exit = True

    def close(self):
        self._dispatch(events.Quit(), immediate=True)
        self.window.close()
        return pyglet.event.EVENT_HANDLED

    def render(self, dt: float):
        """
        Render calculations
        """
        scene = self.engine.current_scene
        if not scene.started:
            return

        if scene is not None:
            # set scene color
            self._bgc = tuple(
                unit / 255 for unit in scene.background_color[:3]
            )

            # Shapes to draw (MOSTLY CIRCLES)
            self.to_draw = []
            dirties = set(scene.dirties)

            if self._load_feedback is not None:
                if not self._load_feedback.loaded:
                    self._load_feedback.text = "RENDERING ENTITIES..."
                    self._load_feedback.loaded = True
                    return

            for entity in dirties:  # type: Union[kge.Sprite, kge.Canvas]
                # Render elements
                shape = entity.renderer.render(scene)
                if shape is not None:
                    self.to_draw.append(shape)

            if self._load_feedback is not None:
                if self._load_feedback.loaded:
                    self._load_feedback.delete()
                    self._load_feedback = None

            cam = self.engine.current_scene.main_camera
            new_win_size = Vector(self.window.width, self.window.height)
            if self.window_size != new_win_size or self._zoom != cam.zoom:
                self._zoom = cam.zoom

                if self.window_size != new_win_size:
                    self.window_size = new_win_size
                    cam.resolution = new_win_size
                    self._dispatch(events.WindowResized(new_size=self.window_size))

    def set2d(self, ):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # gluOrtho2D(0, self.window.width, 0, self.window.height)
        width, height = self.window.width, self.window.height
        glOrtho(-width / 2, width / 2, -height / 2, height / 2, -255, 255)
        # glOrtho(0, window.width, 0, window.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw(self):
        """
        Draw the window
        """
        now = time.monotonic()
        cam = self.engine.current_scene.main_camera

        if now - self.last_step >= 1:
            self.FPS = self.fps
            self.last_step = time.monotonic()
            self.fps = 0
        self.fps += 1

        # Clear the screen
        self.window.clear()
        glClearColor(*self._bgc, 1)

        # Push the Matrix and Translate ViewPort
        glPushMatrix()
        self.set2d()
        # FIXME : NOT SYNCED WITH CAMERA POSITION ?
        # print(f"Camera Pos (Draw: {time.monotonic()})", cam.position)
        glTranslatef(*cam.unit_to_pixels(Vector(
            -cam.position.x,
            cam.position.y,
        )), 0)
        # Set ZOOM
        glScalef(cam.zoom, cam.zoom, cam.zoom)

        # Draw the current Batch
        self.batch.draw()
        for shape, mode in self.to_draw:
            glPointSize(2.0)
            shape.draw(mode)
            glPointSize(1.0)

        # Draw physics data
        if self.logger.getEffectiveLevel() == logging.DEBUG:
            debug = kge.DebugDraw
            debug.world_batch.draw()
            debug.debug_batch.draw()

        glPopMatrix()

        # Display Debug Console
        if self.display_console:
            self.show_console(f"{self.FPS}")

        # Draw the feedback
        if self._load_feedback is not None:
            self._load_feedback.draw(self.window)

        self.imgui_impl.render(imgui.get_draw_data())

        return pyglet.event.EVENT_HANDLED

    def show_console(self, fps: str):
        """
        Show the console
        """
        # SIMPLE OUTPUT
        val = self.output.getvalue()
        if len(val) > 0:
            self.output.truncate(0)
            self.output.seek(0)
            self._console.add_output(val)

        # Log Output
        val = self.log_output.getvalue()
        if len(val) > 0:
            self.log_output.truncate(0)
            self.log_output.seek(0)
            self._console.add_log(val)

        # Error Output
        val = self.err_output.getvalue()
        if len(val) > 0:
            self.err_output.truncate(0)
            self.err_output.seek(0)
            self._console.add_error(val)

        self._console.render(fps)


class Window(Service):
    system_class = Renderer
    _system_instance: Renderer

    @property
    def window(self) -> pyglet.window.Window:
        return self._system_instance.window

    # FIXME : FULLSCREEN NOT WORKING PROPERLY ?
    @property
    def fullscreen(self) -> bool:
        return self._system_instance.window.fullscreen

    @fullscreen.setter
    def fullscreen(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Fullscreen should be a bool")
        self._system_instance.window.set_fullscreen(value, width=self.window.width, height=self.window.height)

    @property
    def batch(self) -> pyglet.graphics.Batch:
        return self._system_instance.batch

    @property
    def render_layers(self) -> List[pyglet.graphics.OrderedGroup]:
        return self._system_instance.layers
