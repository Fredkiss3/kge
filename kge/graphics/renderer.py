import io
import logging
import sys
import time
from typing import Union, List, Optional, Tuple, Callable

import imgui
import pyglet
from imgui.integrations.pyglet import PygletRenderer
from pyglet.gl import *
from pyglet.gl import gl_info as info

import kge
from kge.core import events
from kge.core.component_system import ComponentSystem
from kge.core.constants import DEFAULT_RESOLUTION, IS_FULLSCREEN, IS_RESIZABLE, DEFAULT_FPS, BLACK, \
    MAX_LAYERS, RED, WHITE, YELLOW
from kge.core.service import Service
from kge.graphics.image import Image
from kge.graphics.render_component import RenderComponent
from kge.utils.color import Color
from kge.utils.dotted_dict import DottedDict
from kge.utils.vector import Vector


class DebugPanel(object):
    """
    Console Used For DEBUG, it aims to wraps IMGUI calls
    """
    input: str = ""
    items: List[Tuple[str, Color]] = []
    output_stream: io.StringIO = io.StringIO()
    scroll_down: bool = False

    # No more than 200 lines
    LIMIT_ITEMS = 200

    def add_log(self, log: str):
        self.items.append((log, YELLOW))

    def add_error(self, error):
        self.items.append((error, RED))

    def add_output(self, output: str):
        self.items.append((output, WHITE))

    def render(self, window: pyglet.window.Window, console: bool, _debug_fun: Callable = None):
        # Imgui Renderer
        imgui.new_frame()
        imgui.set_next_window_position(0, 18)
        imgui.set_next_window_size(window.width, window.height - 18)
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_var(imgui.STYLE_ALPHA, 0.01)
        window_flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | \
                       imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | \
                       imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS | \
                       imgui.WINDOW_NO_DOCKING
        imgui.begin('DockSpace', True, window_flags)
        imgui.pop_style_var(4)
        imgui.push_style_var(imgui.STYLE_ALPHA, 1)
        imgui.dock_space("Window Dock Space", 0., 0., 1 << 3)
        imgui.pop_style_var(1)

        imgui.begin("Debug Panel", False, imgui.WINDOW_NO_FOCUS_ON_APPEARING)
        if imgui.begin_main_menu_bar():
            # first menu dropdown
            if imgui.begin_menu('File'):
                clicked, _ = imgui.menu_item('Close')
                if clicked:
                    window.close()
                imgui.end_menu()

            imgui.end_main_menu_bar()

        # Show Everything
        if _debug_fun is not None and callable(_debug_fun):
            _debug_fun()

        if console:
            self._show_input_line()
            self._show_text_output()

        self._show_hardware_infos()

        imgui.end()
        imgui.end()

        # Render Imgui
        imgui.render()

    def _show_hardware_infos(self):
        # [SECTION] HARDWARE INFOS
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 5)
        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (10, 10))
        imgui.set_next_window_size(330, 70)
        window_flags = imgui.WINDOW_NO_TITLE_BAR | \
                       imgui.WINDOW_NO_COLLAPSE | \
                       imgui.WINDOW_NO_RESIZE | \
                       imgui.WINDOW_NO_FOCUS_ON_APPEARING

        imgui.begin("HARDWARE INFOS", False, window_flags)
        imgui.text(f'OpenGL Version: {info.get_version()}')
        imgui.text(f'Vendor: {info.get_vendor()}')
        imgui.text(f'Renderer : {info.get_renderer()}')
        imgui.pop_style_var(3)
        imgui.end()

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
        imgui.push_item_width(150)
        changed, self.input = imgui.input_text(
            'Filter',
            self.input,
            256
        )
        imgui.pop_item_width()

        imgui.end_child()

    def _show_text_output(self):
        # [SECTION] LINE
        imgui.begin_child(
            "TEXT OUTPUT", border=True,
            flags=imgui.WINDOW_HORIZONTAL_SCROLLING_BAR)

        if len(self.items) > self.LIMIT_ITEMS:
            self.items.clear()

        items = filter(lambda i: self.input.lower() in i[0].lower(), self.items)
        for item, color in items:
            # if self.input.lower() in item.lower():
            imgui.text_colored(item, *[c / 255 for c in color])

        if self.scroll_down or imgui.get_scroll_y() >= imgui.get_scroll_max_y():
            imgui.set_scroll_here(1.0)

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
        self.entered = False
        self.loaded = False


class Renderer(ComponentSystem):
    """
    The system which task is to render all elements in a scene
    TODO:
        - Set Pixel Ratio Dynamically
        - Set FullScreen by script --> WIP
        - Resize Window by script --> WIP
        - LOOK FOR 'pyglet Z ordering with Sprite' -> For Applying 'Order in layer' (?)
    """

    def __init__(self,
                 resolution=DEFAULT_RESOLUTION,
                 show_output=False,
                 show_fps=False,
                 fullscreen=IS_FULLSCREEN, resizable=IS_RESIZABLE, vsync=False,
                 **_):
        super().__init__(**_)

        # Show Debug Console
        self.display_log = show_output
        self.display_fps = show_fps

        # String IO for console debugging
        self.err_output = io.StringIO()
        self.output = io.StringIO()

        # Debug Console
        self._console = DebugPanel()

        # To Draw
        self.to_draw = []

        self.components_supported = (RenderComponent,)
        self.accumulated_time = 0
        self.last_tick = None
        self.start_time = None
        self.time_step = 1 / DEFAULT_FPS
        self.window = None  # type: Union[pyglet.window.Window, None]
        self.resolution = resolution
        self._vsync = vsync

        # FIXME : THESE ATTRIBUTES DO NOT WORK PROPERLY
        self._is_fullscreen = fullscreen
        self._is_resizable = resizable

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

        # Camera Position
        self.cam_transform = DottedDict(zoom=1, pos=Vector.Zero())

        # Mean of renders
        self.sum = 0
        self.n_render = 0
        # Elements rendered at each pass
        self._dirties = 0

        # Time took to draw a batch
        self.draw_time = 0
        self.draws = 0

    def on_window_resized(self, event: events.WindowResized, dispatch):
        """
        TODO
        :param event:
        :param dispatch:
        :return:
        """
        pass

    def _show_metrics(self):
        """
        Show Metrics
        """
        imgui.begin_child(
            "METRICS", height=100, border=True, flags=imgui.WINDOW_HORIZONTAL_SCROLLING_BAR)

        draw_call = 1 if self.draws == 0 else (self.draw_time / self.draws) * 1000
        imgui.text(f"""
Entities in scene : {len(self.engine.current_scene.all)} | {len(self.engine.current_scene.dirties)} elements rendered 
DRAW FPS : {self.FPS} | {draw_call} ms took to draw one frame
UPDATE TIME : {self.engine.update_dt * 1000:.4f} ms -> {1 / self.engine.update_dt:.2f} FPS
PHYSICS TIME : {self.engine.fixed_dt * 1000:.4f} ms -> {1 / self.engine.fixed_dt:.2f} FPS
RENDER TIME : {self.engine.render_dt * 1000:.4f} ms -> {self.engine.render_dt * self._dirties * 1000:.4f} ms total""")
        imgui.end_child()

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

        # Load the feedback
        self._load_feedback = LoadingFeedBack()
        with self._load_feedback:
            pass

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
        self.window.set_location(50, 50)

        # show console ?
        if self.display_log:
            sys.stdout = self.output
            sys.stderr = self.err_output

        # Minimum size only if resizable
        if self._is_resizable:
            self.window.set_minimum_size(200, 200)

        # Batch for drawing
        self.batch = pyglet.graphics.Batch()

        # Window events
        self.window.on_draw = lambda: self.on_draw()
        self.window.on_close = lambda: self.close()

        # Enable Alpha transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # create imgui context
        imgui.create_context()
        imgui.get_io().config_flags |= imgui.CONFIG_DOCKING_ENABLE
        self.imgui_impl = PygletRenderer(self.window)

        # Loading FeedBack
        self._load_feedback = LoadingFeedBack()
        with self._load_feedback:
            pass

        # Schedule render update to the time step
        # pyglet.clock.schedule_interval(self.render, self.time_step)
        pyglet.clock.schedule(self.render)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.engine.event_loop.has_exit = True
        self.imgui_impl.shutdown()

    def on_quit(self, ev: events.Quit, dispatch):
        if self.engine is not None:
            self.engine.event_loop.has_exit = True

    def close(self):
        # self._dispatch(events.Quit(), immediate=True)
        self.window.close()
        return pyglet.event.EVENT_HANDLED

    def render(self, dt: float):
        """
        Render calculations
        """
        self.logger.debug("Calling Renderer.render")

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
            self._dirties = len(dirties)

            if self._load_feedback is not None:
                if not self._load_feedback.loaded:
                    self._load_feedback.text = "RENDERING ENTITIES..."
                    self._load_feedback.loaded = True
                    return

            n_render = 0
            sum_ = 0

            self.n_render += 1

            for entity in dirties:  # type: Union[kge.Sprite, kge.Canvas]
                # Render elements
                dep = time.monotonic()
                shape = entity.renderer.render(scene)
                t = time.monotonic() - dep
                n_render += 1
                sum_ += t
                # print(f"Took {t} sec to render {entity}")
                if shape is not None:
                    self.to_draw.append(shape)

            if self._dirties > 0:
                dt = sum_ / n_render
                self.sum += dt
                self.engine.render_dt = self.sum / self.n_render

            if self._load_feedback is not None:
                scene.rendered = True
                if self._load_feedback.loaded:
                    self._load_feedback.delete()
                    self._load_feedback = None

            cam = self.engine.current_scene.main_camera
            self.cam_transform.zoom = cam.zoom
            self.cam_transform.pos = cam.unit_to_pixels(Vector(-cam.position.x, cam.position.y))
            new_win_size = Vector(self.window.width, self.window.height)
            if self.window_size != new_win_size or self._zoom != cam.zoom:
                self._zoom = cam.zoom

                if self.window_size != new_win_size:
                    self.window_size = new_win_size
                    cam.resolution = new_win_size
                    self._dispatch(events.WindowResized(new_size=self.window_size))

            if self.logger.getEffectiveLevel() == logging.DEBUG:
                debug = kge.DebugDraw
                debug.rebatch()
                self._dispatch(events.DrawDebug())

    def set2d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-self.window.width / 2, self.window.width / 2, -self.window.height / 2, self.window.height / 2)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_draw(self):
        """
        Draw the window
        """
        now = time.monotonic()

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

        # Translate to camera
        glTranslatef(*self.cam_transform.pos, 0)

        # Set ZOOM
        glScalef(self.cam_transform.zoom, self.cam_transform.zoom, 0)

        # Draw the current Batch
        self.logger.debug("Calling Renderer.on_draw")
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

        # Display Debug Panel
        if self.display_log or self.display_fps:
            self.show_debug_panel()

        # Draw the feedback
        if self._load_feedback is not None:
            self._load_feedback.draw(self.window)

        self.imgui_impl.render(imgui.get_draw_data())

        # Calculate draw time
        self.draw_time += time.monotonic() - now
        self.draws += 1

        return pyglet.event.EVENT_HANDLED

    def show_debug_panel(self):
        """
        Show the console
        """
        # SIMPLE OUTPUT
        val = self.output.getvalue()
        if len(val) > 0:
            self.output.truncate(0)
            self.output.seek(0)
            self._console.add_output(val)

        # Error Output
        val = self.err_output.getvalue()
        if len(val) > 0:
            self.err_output.truncate(0)
            self.err_output.seek(0)
            self._console.add_error(val)

        self._console.render(self.window, self.display_log, self._show_metrics)


class Window(Service):
    system_class = Renderer
    _system_instance: Renderer

    #: The default mouse cursor.
    CURSOR_DEFAULT = None
    #: A crosshair mouse cursor.
    CURSOR_CROSSHAIR = 'crosshair'
    #: A pointing hand mouse cursor.
    CURSOR_HAND = 'hand'
    #: A "help" mouse cursor; typically a question mark and an arrow.
    CURSOR_HELP = 'help'
    #: A mouse cursor indicating that the selected operation is not permitted.
    CURSOR_NO = 'no'
    #: A mouse cursor indicating the element can be resized.
    CURSOR_SIZE = 'size'
    #: A mouse cursor indicating the element can be resized from the top
    #: border.
    CURSOR_SIZE_UP = 'size_up'
    #: A mouse cursor indicating the element can be resized from the
    #: upper-right corner.
    CURSOR_SIZE_UP_RIGHT = 'size_up_right'
    #: A mouse cursor indicating the element can be resized from the right
    #: border.
    CURSOR_SIZE_RIGHT = 'size_right'
    #: A mouse cursor indicating the element can be resized from the lower-right
    #: corner.
    CURSOR_SIZE_DOWN_RIGHT = 'size_down_right'
    #: A mouse cursor indicating the element can be resized from the bottom
    #: border.
    CURSOR_SIZE_DOWN = 'size_down'
    #: A mouse cursor indicating the element can be resized from the lower-left
    #: corner.
    CURSOR_SIZE_DOWN_LEFT = 'size_down_left'
    #: A mouse cursor indicating the element can be resized from the left
    #: border.
    CURSOR_SIZE_LEFT = 'size_left'
    #: A mouse cursor indicating the element can be resized from the upper-left
    #: corner.
    CURSOR_SIZE_UP_LEFT = 'size_up_left'
    #: A mouse cursor indicating the element can be resized vertically.
    CURSOR_SIZE_UP_DOWN = 'size_up_down'
    #: A mouse cursor indicating the element can be resized horizontally.
    CURSOR_SIZE_LEFT_RIGHT = 'size_left_right'
    #: A text input mouse cursor (I-beam).
    CURSOR_TEXT = 'text'
    #: A "wait" mouse cursor; typically an hourglass or watch.
    CURSOR_WAIT = 'wait'
    #: The "wait" mouse cursor combined with an arrow.
    CURSOR_WAIT_ARROW = 'wait_arrow'

    # Current Cursor
    _cursor = CURSOR_DEFAULT

    @property
    def window(self) -> pyglet.window.Window:
        return self._system_instance.window

    # FIXME : FULLSCREEN NOT WORKING PROPERLY ?
    @classmethod
    def get_fullscreen(self) -> bool:
        return self._system_instance.window.fullscreen

    @classmethod
    def set_fullscreen(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Fullscreen should be a bool")
        self.window.maximize()
        self._system_instance.window.set_fullscreen(value, width=self.window.width, height=self.window.height)

    @classmethod
    def get_cursor(self):
        return self._cursor

    @classmethod
    def set_icon(self, image: Image):
        """
        Set window Icon
        """
        if not isinstance(image, Image):
            raise TypeError("Icon should be an Image")
        self._system_instance.window.set_icon(image.load())

    @classmethod
    def set_cursor(self, value: Union[str, Image]):
        if not isinstance(value, (str, Image)):
            raise TypeError("Cursor should be a str or an Image")
        if isinstance(value, Image):
            cursor = pyglet.window.ImageMouseCursor(value.load())
        else:
            _cursors = [
                self.CURSOR_CROSSHAIR,
                self.CURSOR_HELP,
                self.CURSOR_NO,
                self.CURSOR_SIZE,
                self.CURSOR_SIZE_UP,
                self.CURSOR_SIZE_UP_RIGHT,
                self.CURSOR_SIZE_RIGHT,
                self.CURSOR_SIZE_DOWN_RIGHT,
                self.CURSOR_SIZE_DOWN,
                self.CURSOR_SIZE_DOWN_LEFT,
                self.CURSOR_SIZE_LEFT,
                self.CURSOR_SIZE_UP_LEFT,
                self.CURSOR_SIZE_UP_DOWN,
                self.CURSOR_SIZE_LEFT_RIGHT,
                self.CURSOR_TEXT,
                self.CURSOR_WAIT,
                self.CURSOR_WAIT_ARROW,
            ]

            if not value in _cursors:
                raise ValueError("This cursor is not a valid cursor")

            cursor = self._system_instance.window.get_system_mouse_cursor(value)
        self._system_instance.window.set_mouse_cursor(cursor)
        self._cursor = value

    @classmethod
    def get_size(self) -> Vector:
        return Vector(self.window.width, self.window.height)

    @classmethod
    def set_size(self, value: Vector):
        if not isinstance(value, Vector):
            raise TypeError("Size should be a vector")
        self.window.set_size(*value)

    @property
    def batch(self) -> pyglet.graphics.Batch:
        return self._system_instance.batch

    @property
    def render_layers(self) -> List[pyglet.graphics.OrderedGroup]:
        return self._system_instance.layers
