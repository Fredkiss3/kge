import logging
from typing import Union

import pyglet

# FIXME: AUDIO DRIVER ERRORS ON LINUX
# pyglet.options['audio'] = ('pulse', 'openal', 'directsound', 'silent')
# print(pyglet.media.drivers.get_audio_driver())

import kge
from kge.resources.assetlib import AbstractAsset

logger = logging.getLogger(__name__)


class Sound(AbstractAsset):
    """
    Asset for sound
    """

    def __init__(self, name: str):
        self.name = name

    def load(self) -> Union[pyglet.media.Source, None]:
        """
        Load and return sound
        """
        try:
            return pyglet.resource.media(self.name,
                                         streaming=True)  # type: pyglet.media.Source
        except EOFError:
            logger.warning(f"The sound File '{self.name}' is empty, it won't play.")
            return None
        except pyglet.resource.ResourceNotFoundException:
            logger.warning(f"The sound File '{self.name}' was not found, it won't play.")
            return None
            # raise OSError(f"The sound File '{self.name}' was not found")

    def play(self, volume: float = 10, loop: bool = False):
        """
        Play the sound
        """
        if not (isinstance(volume, (int, float)) and isinstance(loop, bool)):
            raise TypeError("Volume should be a number and loop should be a bool")
        audio = kge.ServiceProvider.getAudio()
        audio.play(self, volume, loop)
