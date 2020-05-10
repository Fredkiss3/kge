"""
https://github.com/Fredkiss3/kge

Copyright (C) 2020-2021 Fredhel KISSIE

THIS GAME ENGINE USE A COMBINATION OF GAME ENGINES :
    - PYGLET : FOR RENDERING AND SOUND SYSTEM
    - PYGAME : FOR JOYSTICK CONTROL

inspired by PPB ENGINE:
Checkout the repository :  https://github.com/ppb/pursuedpybear/
"""
#: The release version
import io

version = '1.1'

import logging
from typing import Callable

from kge.audio.audio_manager import Audio
from kge.audio.sound import Sound
from kge.core import events
from kge.core.behaviour import Behaviour
from kge.core.camera import Camera
from kge.core.component import Component
from kge.core.constants import *
from kge.core.entity import Entity
from kge.core.events import Event
from kge.core.scene import Scene
from kge.core.service_provider import ServiceProvider
from kge.engine import Engine
from kge.graphics.animation import Animation, Frame
from kge.graphics.animator import Animator, ANY
from kge.graphics.image import Image, TiledImage
from kge.graphics.renderer import Window
from kge.graphics.shapes import (Circle, Triangle, Square, Shape, OutlinedCircle, OutLinedSquare,
                                 OutlinedTriangle)
from kge.graphics.sprite import Sprite
from kge.inputs import keys as Keys
from kge.inputs import mouse as Mouse
from kge.inputs.input_manager import Inputs
from kge.physics.colliders import (
    Collider, BoxCollider, CircleCollider, PolygonCollider, SegmentCollider, TriangleCollider,
    EdgeCollider
)
from kge.physics.physics_manager import (
    RayCastInfo, OverlapInfo, Physics, DebugDraw
)
from kge.physics.rigid_body import RigidBody, RigidBodyType
from kge.ui.button import Button, ButtonStyle
from kge.ui.canvas import Canvas
from kge.ui.font import Font
from kge.ui.panel import Panel
from kge.ui.text import Text
from kge.utils.color import Color
from kge.utils.condition import Condition, C
from kge.utils.spatial_hash import Box
from kge.utils.vector import Vector

__all__ = [
    # Run function
    "run",

    # Services
    "Physics",
    "Audio",
    "Window",
    "Inputs",
    "DebugDraw",

    # Animation
    "Frame",
    "Animation",
    "Animator",
    "ANY",

    # Conditions (Mostly used for animations)
    "C",
    "Condition",
    "ALWAYS",

    # Core elements
    "Scene",
    "Behaviour",
    "Component",
    "Camera",

    # Packages
    "resources",
    "utils",
    "audio",
    "events",

    # event class
    "Event",

    # Inputs
    "Keys",
    "Mouse",

    # Utils
    "Vector",

    # Assets
    "Sound",
    "Image",
    "TiledImage",
    "Box",

    # Physics Components & Utils
    "RigidBody",
    "RigidBodyType",
    "BoxCollider",
    "Collider",
    "PolygonCollider",
    "CircleCollider",
    "TriangleCollider",
    "SegmentCollider",
    "EdgeCollider",
    "RayCastInfo",
    "OverlapInfo",

    # Service Locator
    "ServiceProvider",

    # Entity Types
    "Sprite",
    "Canvas",
    "Entity",
    "Empty",

    # UI elements
    "Text",
    "Button",
    "Panel",

    # UI Assets
    "Font",
    "ButtonStyle",

    # Shapes
    "Shape",
    "Square",
    "Triangle",
    "OutLinedSquare",
    "OutlinedTriangle",
    "Circle",
    "OutlinedCircle",

    # Colors
    "Color",
    "RED",
    "BLUE",
    "GREEN",
    "BLACK",
    "WHITE",
    "MAGENTA",
    "GREY",
    "YELLOW",
    "LIGHTGREY",
    "DARKGREY",
    "PURPLE",
    "DEFAULT_PIXEL_RATIO",
]


class Empty(Entity):
    """
    To Create an empty entity (Entity Which have zero for scale)
    """

    def __new__(cls, *args,
                name: str = None,
                tag: str = None,
                **kwargs):
        inst = super().__new__(cls, name=name, tag=tag)
        inst.scale = Vector.Zero()
        return inst


def _make_kwargs(setup, title, engine_opts):
    kwargs = {
        "scene_kwargs": {
            "set_up": setup,
        },
        "window_title": title,
        **engine_opts
    }
    # print(kwargs)
    return kwargs


def run(
        setup: Callable[[Scene], None] = None, *,
        log_level=logging.WARNING,
        starting_scene=Scene,
        title="Kiss Game Engine",
        resizable=True,
        show_output=False,
        show_fps=False,
        resolution=DEFAULT_RESOLUTION,
        fullscreen=False,
        vsync=False,
        pixel_ratio=DEFAULT_PIXEL_RATIO,
        **engine_opts):
    """
    Run a game.

    The resolution will be 1000 pixels wide by 700 pixels be default.

    setup is a callable that accepts a scene and returns None.

    log_level let's you set the expected log level. Consider logging.DEBUG if
    something is behaving oddly.

    starting_scene let's you change the scene used by the engine.
    """
    # output = io.StringIO()
    # if show_log:
    #     logging.basicConfig(level=log_level, stream=output)
    # else:
    logging.basicConfig(level=log_level)

    with make_engine(setup,
                     starting_scene=starting_scene,
                     title=title,
                     pixel_ratio=pixel_ratio,
                     fullscreen=fullscreen,
                     resizable=resizable,
                     show_output=show_output,
                     show_fps=show_fps,
                     # console_output=output,
                     vsync=vsync,
                     resolution=resolution,
                     **engine_opts) as eng:
        eng.run()


def make_engine(setup: Callable[[Scene], None] = None, *,
                starting_scene=Scene, title="Kiss Game Engine",
                **engine_opts):
    return Engine(starting_scene, **_make_kwargs(setup, title, engine_opts))
