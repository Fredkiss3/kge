from typing import Union

import pyglet

import kge
from kge.ui.font import Font
from kge.ui.ui_element import UIElement
# from kge.utils.vector import Vector


class Text(UIElement):
    """
    A text element
    """

    def __init__(self, value: str = '', font: Font = Font()):
        """
       Initialize a text
       :param text: the text value of the text
       :param font: the font applied to the text
        """
        super().__init__()

        # gui values
        self._font = None
        self._text = ""

        # label for pyglet
        self._widget = None  # type: Union[pyglet.text.Label, None]

        # Set properties
        self.text = value
        self.font = font

    def delete(self):
        if self._widget is not None:
            self._widget.delete()
            self._widget = None

    def render(self, scene: 'kge.Scene'):
        """
        Render the text
        """
        super().render(scene)

        if self._visible:
            # Get Positions
            camera = scene.main_camera
            pos = self.screen_position(camera)

            # load font
            self._font.load()

            if self._widget is None:
                renderer = kge.ServiceProvider.getWindow()
                batch = renderer.batch
                layer = renderer.render_layers[self.parent.layer]
                self._widget = pyglet.text.Label(self.text,
                                                 x=pos.x,
                                                 y=pos.y,
                                                 width=camera.unit_to_pixels(self.size.x),
                                                 # height=camera.unit_to_pixels(self.size.y),
                                                 font_name=self.font.name,
                                                 align=self.font.align,
                                                 font_size=self.font.size,
                                                 bold=self.font.weight,
                                                 italic=self.font.style,
                                                 color=(*self.font.color,),
                                                 multiline=True,
                                                 batch=batch,
                                                 group=layer,
                                                 anchor_x='center',
                                                 anchor_y='center',
                                                 )
            else:
                self._widget.text = self.text
                self._widget.x = pos.x
                self._widget.y = pos.y
                self._widget.font_size = self.font.size * camera.zoom
                self._widget.color = (*self.font.color,)
                self._widget.bold = self.font.weight
                self._widget.italic = self.font.style
                self._widget.align = self.font.align
                self._widget.width = camera.unit_to_pixels(self.size.x)
                # self._widget.height = camera.pixels_to_unit(self.size.y)
                self._widget.font_name = self.font.name

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val: str):
        if not isinstance(val, str):
            raise TypeError("The value of the property 'text' should be a string")

        self._text = val
        self.append_to_render_list()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, val: Font):
        if not isinstance(val, Font):
            raise TypeError("The value of the property 'font' should be of type Font (kge.Font)")

        self._font = val
        self.append_to_render_list()
