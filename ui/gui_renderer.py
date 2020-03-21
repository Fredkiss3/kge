from typing import Union

import pyglet

import kge
from kge.graphics.render_component import RenderComponent


class TextRenderer(RenderComponent):
    """
    TODO : Reformat this for canvas
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = None  # type: Union[pyglet.text.Label, None]

    def delete(self):
        if self.label is not None:
            self.label.delete()

    def render(self, scene: kge.Scene):

        camera = scene.main_camera
        pos = camera.world_to_screen_point(self.entity.position)

        renderer = kge.ServiceProvider.getWindow()
        batch = renderer.batch
        layer = renderer.render_layers[self.entity.layer]

        if self.label is None:
            self.label = pyglet.text.Label(self.entity.value, x=pos.x, y=pos.y,
                                           font_size=self.entity.font_size, bold=self.entity.bold,
                                           color=self.entity.color, batch=batch, group=layer)

        else:
            self.label.text = self.entity.value
            self.label.x = pos.x
            self.label.y = pos.y
            self.label.font_size = self.entity.font_size * camera.zoom
            self.label.color = self.entity.color
            self.label.bold = self.entity.bold
