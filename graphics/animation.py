from kge import Image
from kge.resources.assetlib import Asset


class Animation(Asset):

    @classmethod
    def from_sequence(cls, *images: Image):
        pass

    @classmethod
    def from_gif(cls, image: Image):
        pass

    @classmethod
    def from_image_grid(cls, image: Image, grid_size: int):
        pass
