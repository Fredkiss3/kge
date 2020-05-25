from typing import Union

import kge
from kge.core.transform import Transform
from kge.utils.vector import Vector


class UIElement(object):
    """
    An element used for ui
    TODO : DYNAMIC POSITION & SIZE
    """
    nbItems = 0

    def __init__(self):
        super().__init__()
        self._size = Vector.Unit()

        # Name of the ui element
        type(self).nbItems +=1
        self.name = f"{type(self).__name__} {type(self).nbItems}"

        # UI order
        # TODO
        self._order = 0

        # zero, corresponding to the center of the element
        self._position = Vector.Zero()
        self._visible = True
        self._enabled = True

        # rerender ?
        self._render = True

        # set the entity
        self._parent = None  # type: Union[kge.Canvas, None]

        # The current transform used for rendering
        self._transform = Transform(None)

    def dispatch_click_events(self):
        """
        Dispatch click event if there is one
        Should be subclassed
        """
        pass

    @property
    def transform(self):
        # Get the transform of the element
        return self._transform

    def set_hover(self):
        """
        Methods that help to hover an ui element
        :return:
        """
        raise NotImplementedError("Must be subclassed to be used")

    def set_click(self):
        """
        Methods that help to click an ui element
        :return:
        """
        raise NotImplementedError("Must be subclassed to be used")

    def set_normal(self):
        """
        Methods that help to click an ui element
        :return:
        """
        raise NotImplementedError("Must be subclassed to be used")

    @property
    def parent(self) -> 'kge.Canvas':
        return self._parent

    @parent.setter
    def parent(self, p: 'kge.Canvas'):
        if not isinstance(p, kge.Canvas):
            raise TypeError(f"The entity attached to a {type(self).__name__} should be a Canvas (kge.Canvas)")

        # set entity
        self._parent = p
        self.append_to_render_list()

    @property
    def has_to_be_rendered(self):
        """
        Should this element be rendered ?
        :return:
        """
        return self._render

    def append_to_render_list(self):
        """
        Append element to render list
        """
        self._render = True
        if self.parent is not None:
            if not self in self.parent.to_render:
                self.parent.to_render.append(self)

    def rel_pos(self, camera: 'kge.Camera', point: Vector):
        """
        get the screen position of a point relative to the parent canvas
        :return:
        """
        if self.parent.fixed:
            return camera.fixed_world_to_screen_point(point)
        else:
            return camera.world_to_screen_point(point)

    def screen_position(self, camera: 'kge.Camera', edge: bool = False):
        """
        get the screen position
        :return:
        """
        if self.parent.fixed:
            return camera.fixed_world_to_screen_point(self.parent.position + self.position)
        else:
            return camera.world_to_screen_point(self.parent.position + self.position)

    def delete(self):
        """
        For deleting vertices & other things on the element
        :return:
        """
        pass

    def render(self, scene: 'kge.Scene'):
        """
        Render the element
        :param canvas: the parent canvas
        :return:
        """
        self._render = False

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val: Vector):
        if not isinstance(val, Vector):
            raise TypeError("Size should be a vector")

        self._size = val
        self.transform.scale = val
        self.append_to_render_list()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val: Vector):
        if not isinstance(val, Vector):
            raise TypeError("Position should be a vector")

        # Positions
        self._position = val
        self.transform.position = self.parent.position + val
        self.append_to_render_list()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("Visible should be a boolean")

        if not val:
            self.delete()
        elif self._visible != val:
            self.append_to_render_list()

        self._visible = val

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("Visible should be a boolean")

        if self._enabled != val:
            self.append_to_render_list()

        self._enabled = val


    def __repr__(self):
        return f"Element {self.name} attached to canvas '{self.parent}'"
