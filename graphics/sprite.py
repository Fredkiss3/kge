from typing import Union, Callable

from kge.utils.dotted_dict import DottedDict

from kge.core.events import Event
from kge.core.entity import BaseEntity
from kge.graphics.sprite_renderer import SpriteRenderer, Shape
from kge.graphics.image import Image


class Sprite(BaseEntity):
    """
    An entity that can be visualised
    """

    def __fire_event__(self, event: Event, dispatch: Callable[[Event], None]):
        super(Sprite, self).__fire_event__(event, dispatch)
        # Dispatch to sprite renderer also
        self.sprite_renderer.__fire_event__(event, dispatch)

    def __init__(self, name: str = None, tag: str = None):
        super().__init__(name, tag)

        # image and renderer
        self.sprite_renderer = SpriteRenderer(self)

    def flipX(self):
        self.transform.scale.x = -self.transform.scale.x

    def flipY(self):
        self.transform.scale.y = -self.transform.scale.y

    @property
    def size(self) -> DottedDict:
        return DottedDict(
            width=self.sprite_renderer.width,
            height=self.sprite_renderer.height,
        )

    @property
    def image(self):
        return self.sprite_renderer.image

    @image.setter
    def image(self, val: Union[Image, Shape]):
        if not isinstance(val, (Image, Shape)):
            raise TypeError(
                f"image should be of type 'kge.Image' or 'kge.Shape'")
        self.sprite_renderer.image = val
