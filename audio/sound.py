
import pyglet
from kge.resources.assetlib import AbstractAsset


class Sound(AbstractAsset):
    """
    Asset for sound
    """
    def __init__(self, name: str):
        self.name = name

    def load(self) ->  pyglet.media.Source:
        """
        Load and return sound
        """
        return pyglet.resource.media(self.name, streaming=False)  # type: pyglet.media.Source
