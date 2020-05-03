from enum import Enum, auto
from typing import Callable, Optional, Union

import pyglet

import kge
from kge.core.constants import WHITE, LIGHTGREY, DARKGREY, GREY, DEFAULT_PIXEL_RATIO
from kge.graphics.image import Image
from kge.graphics.shapes import Square
from kge.graphics.sprite_renderer import make_pixelated
from kge.ui.font import Font
from kge.ui.ui_element import UIElement
from kge.utils.color import Color
from kge.utils.vector import Vector


class ButtonState(Enum):
    CLICKED = auto()
    HOVERED = auto()
    NORMAL = auto()


class ButtonStyle(object):
    def __init__(self,
                 # Images
                 bg: Image = None,
                 bg_hover: Image = None,
                 bg_clicked: Image = None,
                 bg_disabled: Image = None,

                 # colors
                 bg_color: Color = WHITE,
                 hover_color: Color = LIGHTGREY,
                 disabled_color: Color = GREY,
                 clicked_color: Color = DARKGREY,
                 ):

        if bg is not None and not isinstance(bg, (Image)):
            raise TypeError(
                "The value of the property 'bg' should be an Image (kge.Image)")

        if bg_hover is not None and not isinstance(bg_hover, (Image)):
            raise TypeError(
                "The value of the property 'bg_hover' should be an Image (kge.Image)")

        if bg_clicked is not None and not isinstance(bg_clicked, (Image)):
            raise TypeError(
                "The value of the property 'bg_clicked' should be an Image (kge.Image)")

        if bg_disabled is not None and not isinstance(bg_disabled, (Image)):
            raise TypeError(
                "The value of the property 'bg_disabled' should be an Image (kge.Image)")

        # Color types check
        if not isinstance(bg_color, Color) or \
                not isinstance(hover_color, Color) or \
                not isinstance(disabled_color, Color) or \
                not isinstance(clicked_color, Color):
            raise TypeError("colors arguments should be of type 'kge.Color'")

        # Images
        self.bg_img = bg  # type: Optional[Image]
        self.bg_hover = bg_hover  # type: Optional[Image]
        self.bg_clicked = bg_clicked  # type: Optional[Image]
        self.bg_disabled = bg_disabled  # type: Optional[Image]

        # Colors
        self.bg_color = bg_color  # type: Color
        self.hover_color = hover_color  # type: Color
        self.clicked_color = clicked_color  # type: Color
        self.disabled_color = disabled_color  # type: Color


class Button(UIElement):
    """
    A button element
    """

    def __init__(self,
                 text: str = 'button',
                 on_clicked: Callable = None,

                 # font style & Button Style
                 font: Font = Font(),
                 style: ButtonStyle = ButtonStyle(),
                 ):
        """
        Initialize a button
        :param text: the text value of the button
        :param font: the font applied to the text of the button
        :param on_clicked: the function to call when the button get clicked
        :param bg: the background image, you can specify a shape if you want,
            default will be a white square
        :param bg_color: background color
        :param hover_color: the color to apply to the button when hovered
        :param bg_hover: the background image when hovered
        """
        super().__init__()

        # state
        self._state = ButtonState.NORMAL

        # default size
        self._size = Vector(2, 1)

        # click function
        self._click_function = None  # type: Optional[Callable]

        # Next Bg images & Vertices
        self._bg_sprite = None  # type: Optional[pyglet.sprite.Sprite]
        self._bg_verts = None  # type: Optional[pyglet.graphics.vertexdomain.VertexList]

        # gui values
        self._font = None  # type: Optional[Font]
        self._text = ""
        self._style = None  # type: Optional[ButtonStyle]

        # label for pyglet
        self._label = None  # type: Union[pyglet.text.Label, None]

        # # Set properties
        self.on_clicked = on_clicked

        # self.bg_color = bg_color
        # self.hover_color = hover_color
        # self.bg = bg

        # self.hover_img = hover_img
        self.text = text
        self.font = font
        self.style = style

    def dispatch_click_events(self):
        if self.on_clicked is not None and self.enabled:
            self.on_clicked()

    def set_hover(self):
        self._state = ButtonState.HOVERED
        self.append_to_render_list()

    def set_click(self):
        self._state = ButtonState.CLICKED
        self.append_to_render_list()

    def set_normal(self):
        self._state = ButtonState.NORMAL
        self.append_to_render_list()

    def delete(self):
        if self._label is not None:
            self._label.delete()
            self._label = None

        if self._bg_verts is not None:
            self._bg_verts.delete()
            self._bg_verts = None

        if self._bg_sprite is not None:
            self._bg_sprite.delete()
            self._bg_sprite = None

    def render_text(self, camera: 'kge.Camera'):
        # Get Positions
        pos = self.screen_position(camera)

        # load font
        self._font.load()

        if self._label is None:
            renderer = kge.ServiceProvider.getWindow()
            batch = renderer.batch

            # print(camera.unit_to_pixels(self.size.x))
            # print(camera.unit_to_pixels(self.size.y))

            # layer = renderer.render_layers[self.parent.layer]
            # On top of all
            layer = pyglet.graphics.OrderedGroup(self.parent.layer + 1)
            self._label = pyglet.text.Label(
                self.text,
                x=pos.x,
                y=pos.y,
                width=camera.unit_to_pixels(self.size.x),
                # height=10,#camera.unit_to_pixels(self.size.y),
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
            self._label.text = self.text
            self._label.x = pos.x
            self._label.y = pos.y
            self._label.font_size = self.font.size
            self._label.color = (*self.font.color,)
            self._label.bold = self.font.weight
            self._label.italic = self.font.style
            self._label.align = self.font.align
            self._label.width = camera.unit_to_pixels(self.size.x)
            self._label.font_name = self.font.name
            self._label.anchor_x = 'center'
            self._label.anchor_y = 'center'
            # self._label.height = camera.pixels_to_unit(self.size.y)

    def draw_shape(self, camera: "kge.Camera"):
        vertices = []

        shape = Square()

        if self.enabled:
            if self._state is ButtonState.NORMAL:
                color = self.style.bg_color
            elif self._state is ButtonState.HOVERED:
                color = self.style.hover_color
            else:
                color = self.style.clicked_color
        else:
            color = self.style.disabled_color

        for v in shape.vertices:
            vertices.extend(
                tuple(self.rel_pos(camera,
                                   (
                                           self.transform *
                                           Vector(v.x * self.size.x, v.y * self.size.y)
                                   )
                                   )
                      )
            )

        # Add to Batch for drawing
        if self._bg_verts is None:
            # Get Batch and layers
            win = kge.ServiceProvider.getWindow()
            batch = win.batch
            layers = win.render_layers
            self._bg_verts = batch.add(shape.num_points, shape.mode, layers[self.parent.layer],
                                       ("v2d/stream", tuple(vertices)),
                                       ("c4Bn/dynamic",
                                        (*color[:],) * shape.num_points)
                                       )  # type: pyglet.graphics.vertexdomain.VertexList
        else:
            # Update vertices
            self._bg_verts.vertices = vertices
            self._bg_verts.colors = (*color,) * shape.num_points

    def set_image(self):
        """
        Set Image
        """
        win = kge.ServiceProvider.getWindow()
        layers = win.render_layers

        if self.enabled:
            if self._state is ButtonState.NORMAL:
                color = self.style.bg_color
                img = self.style.bg_img
            elif self._state is ButtonState.HOVERED:
                color = self.style.hover_color
                img = self.style.bg_hover
            else:
                color = self.style.clicked_color
                img = self.style.bg_clicked
        else:
            color = self.style.disabled_color
            img = self.style.bg_disabled

        # Set Sprite & delete vertices
        if img is not None:
            self._bg_sprite = pyglet.sprite.Sprite(
                img=img.load(),
                subpixel=True,
                group=layers[self.parent.layer]
            )

            # Make these pixelated
            make_pixelated(self._bg_sprite)

            # Set scales
            scale_x = DEFAULT_PIXEL_RATIO / (self._bg_sprite.width / self.size.x)
            scale_y = DEFAULT_PIXEL_RATIO / (self._bg_sprite.height / self.size.y)

            self._bg_sprite.update(
                scale_x=scale_x,
                scale_y=scale_y,
            )

            if self._bg_verts is not None:
                self._bg_verts.delete()
                self._bg_verts = None

        elif img is None and self._bg_sprite is not None:
            # self._bg_sprite.opacity = color.alpha * 255
            self._bg_sprite.color = color[:3]

    def render_bg(self, camera: 'kge.Camera'):
        """
        Render Background
        """
        win = kge.ServiceProvider.getWindow()
        batch = win.batch

        # values
        pos = self.screen_position(camera)

        # Set Image
        self.set_image()

        # Draw
        if self._bg_sprite is None:
            if not self._visible:
                self.delete()
            else:
                self.draw_shape(camera)
        else:
            if not self._visible:
                if self._bg_sprite.batch is not None:
                    self._bg_sprite.batch = None
            else:
                if self._bg_sprite.batch is None:
                    self._bg_sprite.batch = batch

                # Scaling
                self._bg_sprite.update(pos.x, pos.y, -self.transform.angle, )

    def render(self, scene: 'kge.Scene'):
        if self._visible:
            self.render_bg(scene.main_camera)
            self.render_text(scene.main_camera)
            pass

    @property
    def on_clicked(self):
        return self._click_function

    @on_clicked.setter
    def on_clicked(self, val: Callable):
        if val is not None and not isinstance(val, Callable):
            raise TypeError("The value of the property 'on_clicked' should be a function")

        self._click_function = val

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

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, val: ButtonStyle):
        if not isinstance(val, ButtonStyle):
            raise TypeError("The value of the property 'style' should be of type ButtonStyle (kge.ButtonStyle)")

        self._style = val
        self.append_to_render_list()


if __name__ == '__main__':
    b = Button()

    b.on_clicked = lambda o: print(o)
    b.on_clicked(7)
