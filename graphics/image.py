import io
import random
from typing import Union

import pyglet

import kge
from kge.resources.assetlib import Asset


class Image(Asset):
    """
    Asset for image
    TODO :
        - Create image from region
    """

    def region(self):
        img = self.load().get_region()
        return NotImplementedError("Not implemented yet")

    def background_parse(self, data) -> pyglet.image.AbstractImage:
        img = pyglet.image.load(self.name, file=io.BytesIO(data))

        # Center the anchor of the image
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        return img

    def file_missing(self) -> pyglet.image.AbstractImage:
        img = pyglet.image.create(64, 64, pyglet.image.CheckerImagePattern())

        # Center the anchor of the image
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        return img
