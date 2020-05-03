from typing import Union, Tuple

import kge
from kge.core.entity import BaseEntity
from kge.graphics.image import Image
from kge.graphics.sprite_renderer import SpriteRenderer, Shape
from kge.utils.color import Color
from kge.utils.dotted_dict import DottedDict


class Sprite(BaseEntity):
    """
    An entity that can be visualised
    """

    def __new__(cls, *args, image: Union[Image, Shape] = None,
                color: Color = None,
                name: str = None, tag: str = None, **kwargs):
        inst = super().__new__(cls, name=name, tag=tag)

        # image and renderer
        inst.renderer = SpriteRenderer(inst)

        # Dispatch Component
        manager = kge.ServiceProvider.getEntityManager()
        manager.dispatch_component_operation(inst, inst.renderer, added=True)

        if image is not None:
            inst.image = image
        if color is not None:
            inst.color = color

        return inst

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

        if self.renderer.image != val:
            self.dirty = True
        self.renderer.image = val

    @property
    def opacity(self):
        return self.renderer.opacity

    @opacity.setter
    def opacity(self, val: float):
        if self.renderer.opacity != val:
            self.dirty = True
        self.renderer.opacity = val

    @property
    def visible(self):
        return self.renderer.visible

    @visible.setter
    def visible(self, val: bool):
        if self.renderer.visible != val:
            self.dirty = True
        self.renderer.visible = val

    @property
    def color(self):
        return self.renderer.color

    @color.setter
    def color(self, val: Union[Tuple[int, int, int], Color]):
        if self.renderer.color != val:
            self.dirty = True
        self.renderer.color = val
