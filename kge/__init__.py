"""
https://github.com/Fredkiss3/kge

Copyright (C) 2020-2021 Fredhel KISSIE

THIS GAME ENGINE USE A COMBINATION OF GAME ENGINES :
    - PYGLET : FOR RENDERING AND SOUND SYSTEM

inspired by PPB ENGINE:
Checkout the repository :  https://github.com/ppb/pursuedpybear/
"""
#: The release version
version = '1.0'

import pyglet_ffmpeg2
import logging
from typing import Callable

from kge.core.service_provider import ServiceProvider
from kge.core.scene import Scene
from kge.core.entity import Entity
from kge.core.component import Component
from kge.core.behaviour import Behaviour
from kge.physics.physics_manager import (
    RayCastInfo, OverlapInfo
)
from kge.physics.rigid_body import RigidBody, RigidBodyType
from kge.physics.colliders import (
    Collider, BoxCollider, CircleCollider, PolygonCollider, EdgeCollider, TriangleCollider,
    LoopCollider
)
from kge.core import events
from kge.physics import events as physics_events
from kge.audio import events as audio_events
from kge.core.events import Event
from kge.utils.vector import Vector
from kge.resources.assetlib import Asset
from kge.audio.sound import Sound
from kge.graphics.image import Image
from kge.graphics.sprite import Sprite
from kge.graphics.tilegrid import TileGrid
from kge.graphics.sprite_renderer import (Circle, Triangle, Square, Shape, OutlinedCircle, OutLinedSquare,
                                          OutlinedTriangle)
from kge.core.camera import Camera
from kge.inputs import keys as Keys
from kge.core.constants import *
from kge.inputs import mouse as Mouse
from kge.ui.text import Text
from kge.core.color import Color

from .engine import Engine

__all__ = [
    # Core elements
    "Scene",
    "Entity",
    "Empty",
    "Behaviour",
    "Component",
    "Camera",

    # Packages
    "resources",
    "utils",
    "audio",
    "events",
    "physics_events",
    "audio_events",

    # event class
    "Event",

    # Inputs
    "Keys",
    "Mouse",

    # Utils
    "Vector",

    # Assets
    "Asset",
    "Sound",
    "Image",

    # Physics Components & Utils
    "RigidBody",
    "RigidBodyType",
    "BoxCollider",
    "Collider",
    "PolygonCollider",
    "CircleCollider",
    "TriangleCollider",
    "EdgeCollider",
    "LoopCollider",
    "RayCastInfo",
    "OverlapInfo",

    # Service Locator
    "ServiceProvider",

    # Sprite Entity
    "Sprite",
    "TileGrid",

    # UI elements
    "Text",

    # Shapes
    "Circle",
    "Shape",
    "Square",
    "Triangle",
    "OutLinedSquare",
    "OutlinedTriangle",
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
]


class Empty(Entity):
    """
    To Create an empty entity
    """

    def __init__(self):
        super().__init__(name="Empty Entity")
        self.transform.scale = Vector.Zero()


def _make_kwargs(setup, title, engine_opts):
    kwargs = {
        "scene_kwargs": {
            "set_up": setup,
        },
        "window_title": title,
        **engine_opts
    }
    return kwargs


def run(setup: Callable[[Scene], None] = None, *, log_level=logging.WARNING,
        starting_scene=Scene, title="Kiss Game Engine", **engine_opts):
    """
    # TODO : ADD NOTICE FOR ARGUMENTS
    Run a game.

    The resolution will be 1000 pixels wide by 700 pixels be default.

    setup is a callable that accepts a scene and returns None.

    log_level let's you set the expected log level. Consider logging.DEBUG if
    something is behaving oddly.

    starting_scene let's you change the scene used by the engine.
    """
    logging.basicConfig(level=log_level, )

    with make_engine(setup, starting_scene=starting_scene, title=title, **engine_opts) as eng:
        eng.run()


def make_engine(setup: Callable[[Scene], None] = None, *,
                starting_scene=Scene, title="Kiss Game Engine",
                **engine_opts):
    return Engine(starting_scene, **_make_kwargs(setup, title, engine_opts))
