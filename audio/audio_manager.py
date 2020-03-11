import pyglet
import pyglet_ffmpeg2

from kge.audio.sound import Sound
from kge.core.service import Service
from kge.core.system import System


class AudioManager(System):
    """
    Audio System
    FIXME : REFACTOR
    """

    def __init__(self, engine=None, **kw):
        super().__init__(engine, **kw)

    def __enter__(self):
        pyglet_ffmpeg2.load_ffmpeg()
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def play(self, snd: Sound, volume: float = 10, loop: bool = False):
        sound = snd.load()  # type: pyglet.media.Source
        player = sound.play()
        player.volume = volume / 10

        # TODO : loop music
        # player.on_eos = lambda *args: print(player.queue(sound), args)


class Audio(Service):
    system_class = AudioManager
    _system_instance: AudioManager

    def play(self, snd: Sound, volume: float=10, loop: bool = False):
        self._system_instance.play(snd, volume, loop)
