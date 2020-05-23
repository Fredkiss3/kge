from kge.graphics.image import Image
from kge.graphics.sprite import Sprite
from kge.graphics.tile_renderer import TileRenderer
from kge.utils.dotted_dict import DottedDict


class TileGrid(Sprite):
    """
    A grid of multiple sprites
    """

    def __init__(self, tile: Image = None, name: str = None, tag: str = None):
        super().__init__(name, tag)

        # image and renderer
        self.sprite_renderer = TileRenderer(self)
        if tile is not None:
            self.tile = tile

    @property
    def image(self):
        raise NotImplementedError("You should use 'tile' property to get the image.")

    @image.setter
    def image(self, val):
        raise NotImplementedError("You should use 'tile' property to set the image.")

    @property
    def tile(self):
        return self.sprite_renderer.image

    @property
    def size(self) -> DottedDict:
        return DottedDict(
            width=self.transform.scale.x,
            height=self.transform.scale.y,
        )

    @tile.setter
    def tile(self, val: Image):
        if not isinstance(val, (Image,)):
            raise TypeError(
                f"image should be of type 'kge.Image'")
        self.sprite_renderer.image = val
