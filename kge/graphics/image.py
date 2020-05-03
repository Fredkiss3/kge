import io
import logging
from typing import List, Dict, Optional

import PIL
import pyglet

from kge.resources.assetlib import AbstractAsset
from kge.utils.dotted_dict import DottedDict
from kge.utils.vector import Vector

logger = logging.getLogger(__name__)


class Image(AbstractAsset):
    """
    Asset for image
    """
    root_folder = None
    _cache = {}  # type: Dict[str, pyglet.image.AbstractImage]

    def __init__(self, path: str):
        self.name = path
        self._size = None

    def is_loaded(self):
        return self.name in Image._cache

    def load(self, **kwargs) -> pyglet.image.AbstractImage:
        file = kwargs.get('file', None)  # type: Optional[io.StringIO]

        # Return Image if on cache
        if file is None and self.name in self._cache:
            return self._cache[self.name]

        if Image.root_folder is not None:
            name = f"{Image.root_folder}/{self.name}"
        else:
            name = self.name
        try:
            img = pyglet.image.load(name, file=file)
        except pyglet.resource.ResourceNotFoundException:
            img = pyglet.image.create(64, 64, pyglet.image.CheckerImagePattern())
        except Exception as e:
            img = pyglet.image.create(64, 64, pyglet.image.CheckerImagePattern())
            logger.error(f"There was an error when reading File '{name}': {e}")

        # Resize the Image
        if self._size is not None:
            print(self._size)
            img.width = int(self._size.x)
            img.height = int(self._size.y)
        else:
            self._size = Vector(img.width, img.height)

        # Center the anchor of the image & add image to cache
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2

        # Add to cache only if file object is not Provided
        if file is None:
            self._cache[self.name] = img
        return img

    def cropped(self, origin: Vector, size: Vector) -> "SlicedImage":
        """
        Get a cropped copy of the image
        """
        return SlicedImage(self.name, DottedDict(origin=origin, size=size))

    def slice(self, sliced_size: Vector) -> List["SlicedImage"]:
        """
        Load Image From Region
        good for sampling sprite sheets
        :param sliced_size: the size of each sample
        """
        img = self.load()

        stepX = img.width // sliced_size.x
        stepY = img.height // sliced_size.y

        images = []
        for x in range(0, stepX):
            for y in range(0, stepY):
                images.append(SlicedImage(self.name, DottedDict(origin=Vector(x * sliced_size.x, y * sliced_size.y),
                                                                size=sliced_size)))

        return images

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: Vector):
        """
        Resize the Image
        """
        if not isinstance(size, Vector):
            raise TypeError("Size Should be a vector")
        self._size = Vector(size)

    def __repr__(self):
        return f"<{type(self).__name__} name={self.name!r}{' loaded' if self.is_loaded() else ''} size={self.size}>"


class SlicedImage(Image):
    """
    A Sliced Image
    """

    def __init__(self, path: str, region: DottedDict = None):
        super().__init__(path)
        self._sliced = False
        self._origin = region.origin
        self._size = region.size

    def load(self) -> pyglet.image.AbstractImage:
        img = super().load()

        if self._origin.x + self._size.x > img.width \
                or self._origin.y + self._size.y > img.height:
            raise ValueError(f"The image {self} is out of the image !")

        img = img.get_region(
            self._origin.x,
            self._origin.y,
            self._size.x,
            self._size.y,
        )

        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        return img

    def __repr__(self):
        return \
            f"""<{type(
                self).__name__} name={self.name!r} region=(origin={self._origin}, size={self._size}) {' loaded' if self.is_loaded() else ''}>"""


class TiledImage(Image):
    """
    A Repeated Image

    Usage :
        >>> tiled = TiledImage(path='image.png', size=Vector(2, 5))

    Where :
        - 'name' is the path of the file
        - 'size' is the number of times we want to repeat the image on x axis and on y axis
    """

    def __init__(self, path: str, size: Vector):
        super().__init__(path)
        # self._io = io.BytesIO()

        size = Vector(int(size.x), int(size.y))  # type: Vector

        if not (size.x > 0 and size.y > 0):
            raise ValueError("Size should be a Vector of integers greater than zero")

        self.tiles = size

    def load(self) -> pyglet.image.AbstractImage:
        from PIL import Image

        # if f"tiled {self.name}" not in self._cache:
        try:
            im1 = PIL.Image.open(self.name)
            im2 = PIL.Image.open(self.name)
            im3 = im1
        except Exception:
            import traceback
            return super().load()
        else:
            for j in range(int(self.tiles.x - 1)):
                im3 = self._get_concat_h(im3, im2)

            for i in range(int(self.tiles.y - 1)):
                im4 = im1
                for j in range(int(self.tiles.x - 1)):
                    im4 = self._get_concat_h(im4, im2)
                im3 = self._get_concat_v(im4, im3)

            format = self.name.split(".")[-1]
            with io.BytesIO() as output:
                im3.save(output, format=format.upper())
                img = super().load(file=output)
                return img

    @staticmethod
    def _get_concat_h(im1, im2):
        from PIL import Image
        dst = PIL.Image.new('RGBA', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst

    @staticmethod
    def _get_concat_v(im1, im2):
        from PIL import Image
        dst = PIL.Image.new('RGBA', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst

    def __repr__(self):
        return \
            f"""<{type(
                self).__name__} name={self.name!r} region=(size={self._size})>"""
