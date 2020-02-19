from typing import Callable

from kge.audio.sound import Sound
from kge.audio import events
from kge.core.events import Event
from kge.core.service import Service

import pyglet_ffmpeg2
from kge.core.system import System


class AudioManager(System):
    """
    Audio System
    FIXME : REFACTOR
    """

    def __init__(self, engine=None, **kw):
        super().__init__(engine, **kw)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def play(self, snd: Sound, loop: bool = False):
        self._dispatch(events.PlaySound(
            sound=snd,
            loop=loop
        ), immediate=True)

    def on_play_sound(self, event: events.PlaySound, dispatch: Callable[[Event], None]):
        pass


class Audio(Service):
    system_class = AudioManager
    _system_instance: AudioManager

    def play(self, snd: Sound, loop: bool = False):
        self._system_instance.play(snd, loop)
