import io
import logging
import random
from typing import Union, List

import pyglet

import kge
from kge.resources.assetlib import AbstractAsset

logger = logging.getLogger(__name__)

class Image(AbstractAsset):
    """
    Asset for image
    TODO :
        - Create image from region
    """
    def __init__(self, name: str):
        self.name = name

    def load(self) -> pyglet.image.AbstractImage:
        try:
            img = pyglet.image.load(self.name)
        except pyglet.resource.ResourceNotFoundException:
            img = pyglet.image.create(64, 64, pyglet.image.CheckerImagePattern())
        except Exception as e:
            img = pyglet.image.create(64, 64, pyglet.image.CheckerImagePattern())
            logger.error(f"There was an error when reading File '{self.name}': {e}")

        # Center the anchor of the image
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        return img

    def region(self, x: int, y: int, width: int, height: int)  -> pyglet.image.AbstractImage:
        """
        Load Image From Region
        TODO
        """
        # img = self.load().get_region()
        raise NotImplementedError("Not implemented yet")

    def slice(self, width: int, height: int)  -> List["Image"]:
        """
        Load Image From Region
        TODO
        """
        # img = self.load().get_region()
        raise NotImplementedError("Not implemented yet")
