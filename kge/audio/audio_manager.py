from typing import List, Tuple, Callable, Dict

import pyglet
# import pyglet_ffmpeg2


from kge.audio.sound import Sound
from kge.core import events
from kge.core.events import Event
from kge.core.service import Service
from kge.core.system import System


class AudioManager(System):
    """
    Audio System
    Note that, we can only use 'wav' and 'ogg' format for sounds
    TODO : POSITIONNAL AUDIO WITH AUDIO SOURCE & OPENAL (?)
    FIXME : SOUND SOMETIMES BUGS WHEN SPAMMING MULTI
    """
    _players: List[pyglet.media.Player] = []
    _args: List[Tuple] = []
    _scheduled: Dict[pyglet.media.Player, Callable] = {}

    def __init__(self, engine=None, **kw):
        super().__init__(engine, **kw)

    def __enter__(self):
        # pyglet_ffmpeg2.load_ffmpeg()
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def on_eos(self, t: Tuple):
        """
        Delete or loop at the end of a sound
        """
        player, sound, loop, snd, pitch, volume = t
        if player.time >= sound.duration:
            self._players.remove(player)
            self._scheduled.pop(player)
            self._args.remove(t)

            if loop:
                self.logger.debug(f"Looping sound : {snd}")
                self.play(snd, volume, loop, pitch)
            else:
                self.logger.debug(f"Deleting from players : {snd}")
        self.logger.debug(f"Calling ON_EOS function with {len(self._players)} players left")

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

            # We must cache these sounds
            self._args.append((player, sound, loop, snd, pitch, volume))

            # I use this in order to replace 'on_player_eos' of player
            self._scheduled[player] = (lambda dt: self.on_eos(self._args[-1]))
            pyglet.clock.schedule_once(self._scheduled[player], sound.duration + .1)

            # In order to keep a reference to the player
            self._players.append(player)

    def on_scene_stopped(self, ev: events.SceneStopped, dispatch: Callable[[Event], None]):
        """
        Unschedule unused players
        """
        for f in self._scheduled:
            pyglet.clock.unschedule(f)

        # Clear all arguments and players
        self._scheduled.clear()
        self._players.clear()
        self._args.clear()

class Audio(Service):
    """
    Note that, we can only use 'wav' and 'ogg' format for sounds
    """
    system_class = AudioManager
    _system_instance: AudioManager

    @classmethod
    def play(self, snd: Sound, volume: float = 10, loop: bool = False, pitch: float = 1):
        if not (isinstance(volume, (int, float)) and isinstance(pitch, (int, float)) and isinstance(loop, bool)):
            raise TypeError("Volume should be a number and loop should be a bool")
        self._system_instance.play(snd, volume, loop, pitch)
