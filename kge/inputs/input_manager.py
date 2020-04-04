from typing import Dict, Type, Union, Callable

from pyglet.window import key as key_ev
from pyglet.window import mouse as mouse_ev

import kge
from kge.core import events
from kge.core.events import Event
from kge.core.service import Service
from kge.core.system import System
from kge.inputs import keys
from kge.inputs import mouse
from kge.inputs.keys import KeyCode
from kge.inputs.mouse import MouseInput, MouseScroll
from kge.utils.vector import Vector


class InputManager(System):
    """
    A system that converts Pyglet events to Kge Events
    TODO :
        - HANDLE JOYSTICK EVENTS
        - FOR AS MANY JOYS AS POSSIBLE (SET A MAX JOYS)
        - JOYSTICK KEY HANDLER (JUST A DICT)

    """

    event_map = None

    mouse_button_map: Dict[int, MouseInput] = {
        mouse_ev.LEFT: mouse.Left,
        mouse_ev.MIDDLE: mouse.Middle,
        mouse_ev.RIGHT: mouse.Right,
    }

    # Keyboard map
    key_map: Dict[int, keys.KeyCode] = {
        key_ev.A: keys.A,
        key_ev.B: keys.B,
        key_ev.C: keys.C,
        key_ev.D: keys.D,
        key_ev.E: keys.E,
        key_ev.F: keys.F,
        key_ev.G: keys.G,
        key_ev.H: keys.H,
        key_ev.I: keys.I,
        key_ev.J: keys.J,
        key_ev.K: keys.K,
        key_ev.L: keys.L,
        key_ev.M: keys.M,
        key_ev.N: keys.N,
        key_ev.O: keys.O,
        key_ev.P: keys.P,
        key_ev.Q: keys.Q,
        key_ev.R: keys.R,
        key_ev.S: keys.S,
        key_ev.T: keys.T,
        key_ev.U: keys.U,
        key_ev.V: keys.V,
        key_ev.W: keys.W,
        key_ev.X: keys.X,
        key_ev.Y: keys.Y,
        key_ev.Z: keys.Z,
        key_ev._1: keys.One,
        key_ev._2: keys.Two,
        key_ev._3: keys.Three,
        key_ev._4: keys.Four,
        key_ev._5: keys.Five,
        key_ev._6: keys.Six,
        key_ev._7: keys.Seven,
        key_ev._8: keys.Eight,
        key_ev._9: keys.Nine,
        key_ev._0: keys.Zero,
        key_ev.F1: keys.F1,
        key_ev.F2: keys.F2,
        key_ev.F3: keys.F3,
        key_ev.F4: keys.F4,
        key_ev.F5: keys.F5,
        key_ev.F6: keys.F6,
        key_ev.F7: keys.F7,
        key_ev.F8: keys.F8,
        key_ev.F9: keys.F9,
        key_ev.F10: keys.F10,
        key_ev.F11: keys.F11,
        key_ev.F12: keys.F12,
        key_ev.F13: keys.F13,
        key_ev.F14: keys.F14,
        key_ev.F15: keys.F15,
        key_ev.NUM_0: keys.NumpadZero,
        key_ev.NUM_1: keys.NumpadOne,
        key_ev.NUM_2: keys.NumpadTwo,
        key_ev.NUM_3: keys.NumpadThree,
        key_ev.NUM_4: keys.NumpadFour,
        key_ev.NUM_5: keys.NumpadFive,
        key_ev.NUM_6: keys.NumpadSix,
        key_ev.NUM_7: keys.NumpadSeven,
        key_ev.NUM_8: keys.NumpadEight,
        key_ev.NUM_9: keys.NumpadNine,
        key_ev.NUM_DIVIDE: keys.NumpadDivide,
        key_ev.NUM_ENTER: keys.NumpadEnter,
        key_ev.NUM_EQUAL: keys.NumpadEquals,
        key_ev.NUM_SUBTRACT: keys.NumpadMinus,
        key_ev.NUM_MULTIPLY: keys.NumpadMultiply,
        key_ev.NUM_DELETE: keys.NumpadDot,
        key_ev.NUM_ADD: keys.NumpadPlus,
        key_ev.RALT: keys.AltRight,
        key_ev.LALT: keys.AltLeft,
        key_ev.BACKSLASH: keys.Backslash,
        key_ev.BACKSPACE: keys.Backspace,
        key_ev.BRACKETLEFT: keys.BracketLeft,
        key_ev.BRACKETRIGHT: keys.BracketRight,
        key_ev.CAPSLOCK: keys.CapsLock,
        key_ev.COMMA: keys.Comma,
        key_ev.LCTRL: keys.CtrlLeft,
        key_ev.RCTRL: keys.CtrlRight,
        key_ev.DELETE: keys.Delete,
        key_ev.DOWN: keys.Down,
        key_ev.END: keys.End,
        key_ev.RETURN: keys.Enter,
        key_ev.EQUAL: keys.Equals,
        key_ev.ESCAPE: keys.Escape,
        key_ev.GRAVE: keys.Grave,
        key_ev.HOME: keys.Home,
        key_ev.INSERT: keys.Insert,
        key_ev.LEFT: keys.Left,
        key_ev.MENU: keys.Menu,
        key_ev.MINUS: keys.Minus,
        key_ev.NUMLOCK: keys.NumLock,
        key_ev.PAGEDOWN: keys.PageDown,
        key_ev.PAGEUP: keys.PageUp,
        key_ev.PAUSE: keys.Pause,
        key_ev.BREAK: keys.Pause,
        key_ev.PERIOD: keys.Period,
        key_ev.PRINT: keys.PrintScreen,
        key_ev.APOSTROPHE: keys.Quote,
        key_ev.RIGHT: keys.Right,
        # key_ev.SCROLLOCK: keys.ScrollLock,
        key_ev.SEMICOLON: keys.Semicolon,
        key_ev.LSHIFT: keys.ShiftLeft,
        key_ev.RSHIFT: keys.ShiftRight,
        key_ev.SLASH: keys.Slash,
        key_ev.SPACE: keys.Space,
        key_ev.LCOMMAND: keys.SuperLeft,
        key_ev.LMETA: keys.SuperLeft,
        key_ev.RCOMMAND: keys.SuperRight,
        key_ev.RMETA: keys.SuperRight,
        key_ev.TAB: keys.Tab,
        key_ev.UP: keys.Up,
    }

    # Modifiers Map (SHIFT, ALT, CTRL, etc)
    mod_map = {
        key_ev.LSHIFT: keys.ShiftLeft,
        key_ev.RSHIFT: keys.ShiftRight,
        key_ev.LCTRL: keys.CtrlLeft,
        key_ev.RCTRL: keys.CtrlRight,
        key_ev.LALT: keys.AltLeft,
        key_ev.RALT: keys.AltRight,
        key_ev.LMETA: keys.SuperLeft,
        key_ev.RMETA: keys.SuperRight,
        key_ev.NUMLOCK: keys.NumLock,
        key_ev.CAPSLOCK: keys.CapsLock
    }

    k_ups = []
    mouse_ups = []
    wheel_up = False
    wheel_down = False
    window_ref = None

    key_handler: Union[None, key_ev.KeyStateHandler] = None
    mouse_handler: Union[None, "mouse_ev.MouseStateHandler"] = None

    def __init__(self, engine=None, **_):
        super().__init__(engine=engine, **_)

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __enter__(self):
        self.key_handler = key_ev.KeyStateHandler()
        self.mouse_handler = mouse_ev.MouseStateHandler()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.key_handler = None
        self.mouse_handler = None

    def on_scene_stopped(self, ev: events.SceneStopped, dispatch: Callable[[Event], None]):
        """
        Remove Window Reference
        """
        self.window_ref = None

    def on_scene_started(self, ev: events.SceneStarted, dispatch: Callable[[Event], None]):
        """
        Attach Handlers when the scene starts
        """
        if self.window_ref is None:
            try:
                window = kge.ServiceProvider.getWindow().window
                window.push_handlers(self.key_handler)
                window.push_handlers(self.mouse_handler)

                # BIND THESE FUNCTIONS
                window.on_key_release = lambda symbol, mods: self.key_up(symbol, mods, ev.scene)
                window.on_key_press = lambda symbol, mods: self.key_down(symbol, mods, ev.scene)
                window.on_mouse_release = lambda x, y, btn, mods: self.mouse_button_released(x, y, btn, mods,
                                                                                             ev.scene)
                window.on_mouse_press = lambda x, y, btn, mods: self.mouse_button_pressed(x, y, btn, mods, ev.scene)
                window.on_mouse_scroll = lambda x, y, left, up: self.mouse_wheel(x, y, left, up, ev.scene)
                window.on_mouse_motion = lambda x, y, dx, dy: self.mouse_motion(x, y, dx, dy, ev.scene)

                window.on_mouse_drag = lambda x, y, dx, dy, buttons, mods: self.mouse_drag(x, y, dx, dy, buttons, mods,
                                                                                           ev.scene)
                window.on_mouse_enter = lambda x, y: self.mouse_enter(x, y, ev.scene)
                window.on_mouse_leave = lambda x, y: self.mouse_exit(x, y, ev.scene)
            except Exception:
                self.logger.warning("This system won't work without renderer system being started first")
            else:
                self.window_ref = window

        # TODO
        # joysticks = pyglet.input.get_joysticks()
        # if joysticks:
        #     joystick = joysticks[0]
        #     joystick.open()
        # joystick.push_handlers()
        # print(joystick)

    def mouse_wheel(self, x, y, left, up, scene: "kge.Scene"):
        """
        Mouse scroll
        """
        # Get screen position of the mouse event
        screen_position = Vector(x, y)
        camera = scene.main_camera

        # Get world (or scene) position of the mouse event
        scene_position = camera.screen_to_world_point(screen_position)

        if up == 1:
            self._dispatch(events.MouseScroll(position=scene_position,
                                              direction=MouseScroll.UP,
                                              screen_position=Vector(x, y)
                                              ))
        elif up == -1:
            self._dispatch(events.MouseScroll(position=scene_position,
                                              direction=MouseScroll.DOWN,
                                              screen_position=Vector(x, y)
                                              ))
        if left == 1:
            self._dispatch(events.MouseScroll(position=scene_position,
                                              direction=MouseScroll.LEFT,
                                              screen_position=Vector(x, y)
                                              ))
        elif left == -1:
            self._dispatch(events.MouseScroll(position=scene_position,
                                              direction=MouseScroll.RIGHT,
                                              screen_position=Vector(x, y)
                                              ))

    def get_mouse_down(self, mouse: Type[MouseInput]):
        """
        Get Mouse Down
        """
        mouse_btn = list(self.mouse_button_map.keys())[list(self.mouse_button_map.values()).index(mouse)]
        return self.mouse_handler[mouse_btn]

    def get_key_down(self, key: Type[KeyCode]):
        """
        Get key down
        """
        key_ = list(self.key_map.keys())[list(self.key_map.values()).index(key)]
        return self.key_handler[key_]

    def mouse_motion(self, x, y, dx, dy, scene: "kge.Scene"):
        """
        Did Mouse Moved ?
        :param event:  event
        :param scene: the scene in which this event occur
        :return:
        """
        # Get screen position of the mouse event
        screen_position = Vector(x, y)
        camera = scene.main_camera

        # Get world (or scene) position of the mouse event
        scene_position = camera.screen_to_world_point(screen_position)
        delta = Vector(dx, dy) * (1 / camera.pixel_ratio)

        self._dispatch(events.MouseMotion(
            position=scene_position,
            screen_position=screen_position,
            delta=delta,
            buttons={}
        ))

    def mouse_drag(self, x, y, dx, dy, btn, mods, scene: "kge.Scene"):
        """
        Did Mouse Moved ?
        :param event:  event
        :param scene: the scene in which this event occur
        :return:
        """
        mouse_btn = self.mouse_button_map.get(btn)

        # Get screen position of the mouse event
        screen_position = Vector(x, y)
        camera = scene.main_camera

        # Get world (or scene) position of the mouse event
        scene_position = camera.screen_to_world_point(screen_position)
        delta = Vector(dx, dy) * (1 / camera.pixel_ratio)

        self._dispatch(events.MouseDrag(
            position=scene_position,
            screen_position=screen_position,
            delta=delta,
            buttons={
                mouse_btn
            }
        ))

    def mouse_button_pressed(self, x, y, btn, mods, scene: "kge.Scene"):
        """
        Did we clicked on mouse button ?
        :param event:  event
        :param scene: the scene in which this event occur
        :return:
        """
        screen_position = Vector(x, y)
        camera = scene.main_camera

        scene_position = camera.world_to_screen_point(screen_position)

        # Get the button clicked
        mouse_btn = self.mouse_button_map.get(btn)
        if mouse_btn is not None:
            self._dispatch(events.MouseDown(
                button=mouse_btn,
                position=scene_position,
                screen_position=screen_position
            ))

    def mouse_button_released(self, x, y, btn, mods, scene: "kge.Scene"):
        """
        Did we released a mouse button ?
        :param event:  event
        :param scene:
        :return:
        """
        screen_position = Vector(x, y)
        camera = scene.main_camera
        scene_position = camera.screen_to_world_point(screen_position)

        mouse_btn = self.mouse_button_map.get(btn)
        if mouse_btn is not None:
            self._dispatch(events.MouseUp(
                button=mouse_btn,
                position=scene_position,
                screen_position=screen_position
            ))

    def key_down(self, symbol, mods, scene: "kge.Scene"):
        """
        Did we just clicked a keyboard button ?
        :param event:  event
        :param scene: the scene in which this event occur
        :return:
        """
        try:
            self._dispatch(events.KeyDown(key=self.key_map[symbol],
                                          mods=self.build_mods(mods)))
        except KeyError:
            pass
        else:
            self.logger.debug(f"{type(self.key_map[symbol])} pressed !")

    def key_up(self, symbol, mods, scene: "kge.Scene"):
        """
        Did we just released a keyboard button ?
        :param event:  event
        :param scene: the scene in which this event occur
        :return:
        """
        try:
            self._dispatch(events.KeyUp(key=self.key_map[symbol],
                                        mods=self.build_mods(mods)))
        except KeyError:
            pass
        else:
            self.logger.debug(f"{type(self.key_map[symbol])} released !")

    def build_mods(self, modifiers):
        return {value for mod, value in self.mod_map.items() if mod & modifiers == 2}

    def mouse_exit(self, x, y, scene: "kge.Scene"):
        """
        When the mouse enter the window
        """
        position = scene.main_camera.screen_to_world_point(Vector(x, y))

        self._dispatch(
            events.MouseLeave(
                position=position,
                screen_position=Vector(x, y)
            )
        )

    def mouse_enter(self, x, y, scene: "kge.Scene"):
        """
        When the mouse exit the window
        """
        position = scene.main_camera.screen_to_world_point(Vector(x, y))

        self._dispatch(
            events.MouseEnter(
                position=position,
                screen_position=Vector(x, y)
            )
        )


class InputService(Service):
    system_class = InputManager
    _system_instance: InputManager

    def get_key_down(self, key: Type[KeyCode]) -> bool:
        """
        Find if the specified key is pressed
        """
        return self._system_instance.get_key_down(key)

    def get_mouse_down(self, mouse_btn: Type[MouseInput]) -> bool:
        return self._system_instance.get_mouse_down(mouse_btn)
