from typing import Union, Callable

from kge.resources.events import AssetLoaded
from kge.utils.dotted_dict import DottedDict

from kge.core.events import Event
from kge.core.entity import BaseEntity
from kge.graphics.sprite_renderer import SpriteRenderer, Shape
from kge.graphics.image import Image


class Sprite(BaseEntity):
    """
    An entity that can be visualised
    FIXME : Migrate all of the events to renderer system
    """

    def on_asset_loaded(self, event: AssetLoaded, dispatch: Callable[[Event], None]):
        # TODO : To remove
        self.sprite_renderer.__fire_event__(event, dispatch)

    def on_disable_entity(self, event, dispatch):
        # TODO : To remove
        self.sprite_renderer.__fire_event__(event, dispatch)

    def on_enable_entity(self, event, dispatch):
        # TODO : To remove
        self.sprite_renderer.__fire_event__(event, dispatch)

    def on_destroy_entity(self, event, dispatch):
        # TODO : To remove
        self.sprite_renderer.__fire_event__(event, dispatch)

    def on_scene_stopped(self, event, dispatch):
        # TODO : To remove
        self.sprite_renderer.__fire_event__(event, dispatch)

    def __init__(self, image: Union[Image, Shape] = None, name: str = None, tag: str = None, ):
        super().__init__(name, tag)

        # image and renderer
        self.sprite_renderer = SpriteRenderer(self)
        if image is not None:
            self.image = image

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
