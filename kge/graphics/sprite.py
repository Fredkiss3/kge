from typing import Union, Callable

import kge
from kge.resources.events import AssetLoaded
from kge.utils.dotted_dict import DottedDict

from kge.core.events import Event
from kge.core.entity import BaseEntity
from kge.graphics.sprite_renderer import SpriteRenderer, Shape
from kge.graphics.image import Image


class Sprite(BaseEntity):
    """
    An entity that can be visualised
    """
    def __init__(self, image: Union[Image, Shape] = None, name: str = None, tag: str = None, ):
        super().__init__(name, tag)

        # image and renderer
        self.renderer = SpriteRenderer(self)

        # Dispatch Component
        manager = kge.ServiceProvider.getEntityManager()
        manager.dispatch_component_operation(self, self.renderer, added=True)

        if image is not None:
            self.image = image

    def flipX(self):
        self.transform.scale.x = -self.transform.scale.x

    def flipY(self):
        self.transform.scale.y = -self.transform.scale.y

    @property
    def size(self) -> DottedDict:
        return DottedDict(
            width=self.renderer.width,
            height=self.renderer.height,
        )

    @property
    def image(self):
        return self.renderer.image

    @image.setter
    def image(self, val: Union[Image, Shape]):
        if not isinstance(val, (Image, Shape)):
            raise TypeError(
                f"image should be of type 'kge.Image' or 'kge.Shape'")
        self.renderer.image = val

    @property
    def opacity(self):
        return self.renderer.opacity

    @opacity.setter
    def opacity(self, val: float):
        self.renderer.opacity = val

    @property
    def visible(self):
        return self.renderer.visible

    @visible.setter
    def visible(self, val: bool):
        self.renderer.visible = val

