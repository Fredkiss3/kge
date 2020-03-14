from typing import List

import pyglet
import pyglet_ffmpeg2

# FIXME: AUDIO ERRORS WITH OPENAL
from kge.audio.sound import Sound
from kge.core.service import Service
from kge.core.system import System


class AudioManager(System):
    """
    Audio System
    TODO : POSITIONNAL AUDIO WITH AUDIO SOURCE
    """
    _players: List[pyglet.media.Player] = []

    def __init__(self, engine=None, **kw):
        super().__init__(engine, **kw)

    def __enter__(self):
        pyglet_ffmpeg2.load_ffmpeg()
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def play(self, snd: Sound, volume: float = 10, loop: bool = False):
        sound = snd.load()  # type: pyglet.media.Source
        if sound is not None:
            # sound.play()

            player = pyglet.media.Player()
            player.volume = volume / 10
            player.queue(sound)
            player.play()

            # TODO : TO REMOVE
            # def _no_loop():
            #     print("No loop")
            #     AudioManager._players.remove(player)
            #     player.on_player_eos = None
            #
            # def _loop():
            #
            #     player.seek(0)
            #     player.queue(sound)
            #     player.play()

            # If loop
            player.loop = loop
            self._players.append(player)

            # TODO : TO REMOVE
            # # Loop or not
            # if loop:
            #     _on_player_eos = _loop
            # else:
            #     _on_player_eos = _no_loop
            #
            # # Append players in order to keep a reference to it
            #
            # self._players[-1].on_eos = _on_player_eos


class Audio(Service):
    system_class = AudioManager
    _system_instance: AudioManager

    def play(self, snd: Sound, volume: float = 10, loop: bool = False):
        self._system_instance.play(snd, volume, loop)
