import kge
from kge.core.entity import BaseEntity
from kge.ui.gui_renderer import TextRenderer
from kge.core.constants import WHITE


class Text(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # gui values
        self._value = ""
        self._font_size = 10
        self._bold = False
        self._color = WHITE

        # renderer component
        self.renderer = TextRenderer(self)


        # Dispatch Component
        manager = kge.ServiceProvider.getEntityManager()
        manager.dispatch_component_operation(self, self.renderer, added=True)


    def on_destroy_entity(self, event, dispatch):
        super().on_destroy_entity(event, dispatch)
        self.renderer.delete()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: str):
        if not isinstance(val, str):
            raise TypeError("Value should be a string")
        self._value = val

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, val: float):
        if not isinstance(val, (int, float)):
            raise TypeError("Font Size should be a number")
        self._font_size = val

    @property
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("Bold should be a boolean")
        self._bold = val

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val: tuple):
        if not isinstance(val, tuple):
            raise TypeError("Color should be a tuple of 4 integer values (R, G, B, A). Example : (125, 125, 125, 125)")
        elif isinstance(val, tuple) and not len(val) == 4:
            raise TypeError("Color should be a tuple of 4 integer values (R, G, B, A). Example : (125, 125, 125, 125)")

        self._color = val
