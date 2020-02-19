import io

import pyglet
import pyglet_ffmpeg2
from kge.resources.assetlib import Asset


class Sound(Asset):
    """
    Asset for sound
    """

    def background_parse(self, data):
        # Return Sound
        return pyglet.media.load(self.name, file=io.BytesIO(data), streaming=False)  # type: pyglet.media.Source
