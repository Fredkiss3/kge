import io
import random
from typing import Union

import pyglet

import kge
from kge.resources.assetlib import Asset


class Image(Asset):
    """
    Asset for image
    TODO : IMPLEMENT 'file_missing' function
    """

    def background_parse(self, data):
        img = pyglet.image.load(self.name, )  # file=io.BytesIO(data))

        # Center the anchor of the image
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        return img

    def file_missing(self):
        # todo : Create a square placeholder image
        raise NotImplementedError("Not Implemented yet")

        # img = pyglet.image.ImageData.create_texture(cls=pyglet.image.Texture, rectangle=True)
        #
        # # Center the anchor of the image
        # img.anchor_x = img.width // 2
        # img.anchor_y = img.height // 2
        # return img
