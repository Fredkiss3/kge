from typing import Callable, Set, Union, Type

import kge.inputs.keys as Keys
from kge.core import events
# from kge.core.component_system import ComponentSystem
# from kge.ui.canvas_renderer import CanvasRenderer
from kge.core.system import System
from kge.utils.vector import Vector
from kge.ui.canvas import Canvas, Clear, ClickDown, ClickUp, Hover, CanvasEvent
from kge.utils.spatial_hash import Box


class UIManager(System):
    """
    A system that dispatch events to canvas
    FIXME : CANVAS SHOULD NOT BE AFFECTED BY ZOOM
    """

    _stated = set() # type: Set[Canvas]
    _searchSize = Vector.Unit() / 32


    def __enter__(self):
        pass

    def on_key_down(self, ev: events.KeyDown, dispatch: Callable):
        # TODO : SHOULD DO SOMETHIN' (?)
        if ev.key is Keys.Up:
            pass
        elif ev.key is Keys.Down:
            pass

    def on_key_up(self):
        # TODO : SHOULD DO SOMETHIN' (?)
        pass


    def dispatch(self, ev:Union[events.MouseMotion, events.MouseDown, events.MouseUp], e: Union[Type[ClickUp], Type[ClickDown], Type[Hover]]):
        # FIXME : IS THIS PERFORMANT ?
        self.clear_canvases()

        canvases = ev.scene.spatial_hash.search(ev.position, self._searchSize, Canvas)

        # For testing if canvas collide with mouse
        box = Box(ev.position,  self._searchSize)

        # Clear all canvases
        for canvas in canvases:  # type: Canvas
            cbox = Box(canvas.position, canvas.scale)
            if box.overlaps(cbox) and canvas.visible:
                canvas.dispatch(e(zone=box))
                self._stated.add(canvas)

    def on_mouse_motion(self, ev: events.MouseMotion, dispatch: Callable):
        self.dispatch(ev, Hover)

    def clear_canvases(self):
        for c in self._stated:
            c.dispatch(Clear())

        self._stated = set()

    def on_mouse_down(self, ev: events.MouseDown, dispatch: Callable):
        self.dispatch(ev, ClickDown)

    def on_mouse_up(self, ev: events.MouseUp, dispatch: Callable):
        self.dispatch(ev, ClickUp)
