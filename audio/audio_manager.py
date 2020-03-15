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

    def play(self, snd: Sound, volume: float = 10, loop: bool = False, pitch: float = 1):
        sound = snd.load()  # type: pyglet.media.Source
        if sound is not None:
            # Create player with pitch and volume
            player = pyglet.media.Player()
            player.volume = volume / 10
            player.pitch = pitch

            # Queue & play sound
            player.queue(sound)
            player.play()

            def on_eos(dt):
                """
                Delete or loop at the end of a sound
                """
                if player.time >= sound.duration:
                    self._players.remove(player)

                    if loop:
                        self.logger.debug(f"Looping sound : {snd}")
                        self.play(snd, volume, loop, pitch)
                    else:
                        self.logger.debug(f"Deleting from players : {snd}")
                self.logger.debug(f"Calling ON_EOS function with {len(self._players)} players left")

            # I use this in order to replace 'on_player_eos' of player
            pyglet.clock.schedule_once(on_eos, sound.duration + .1)

            # In order to keep a reference to the player
            self._players.append(player)


class Audio(Service):
    system_class = AudioManager
    _system_instance: AudioManager

    def play(self, snd: Sound, volume: float = 10, loop: bool = False, pitch: float = 1):
        if not (isinstance(volume, (int, float)) and isinstance(pitch, (int, float)) and isinstance(loop, bool)):
            raise TypeError("Volume should be a number and loop should be a bool")
        self._system_instance.play(snd, volume, loop, pitch)
