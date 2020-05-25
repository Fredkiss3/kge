from typing import Optional

import kge
from kge.core import events
from kge.graphics.render_component import RenderComponent
from kge.ui.ui_element import UIElement
from kge.utils.vector import Vector


class CanvasRenderer(RenderComponent):
    """
    A component that handles the rendering of the canvas
    """

    def __init__(self, entity: 'kge.Canvas'):
        self._entity = None  # type: Optional[kge.Canvas]
        super().__init__(entity)

    def render(self, scene: "kge.Scene"):
        """
        Render all ui components that needs to be rendered
        """
        if self.entity.is_active and self.entity.visible:
            if self.entity.fixed:
                in_frame = scene.main_camera.in_frame(self.entity)
                if in_frame:
                    while self.entity.to_render:
                        element = self.entity.to_render.popleft()
                        element.render(scene)
                else:
                    self.delete(redraw=True)
            else:
                in_frame = scene.main_camera.in_frame(self.entity)
                if in_frame:
                    for e in self.entity.spatial_hash.search(Vector.Zero(),
                                                             self.entity.scale + Vector.Unit() / 3):  # type: UIElement
                        e.render(scene)
                else:
                    self.delete(redraw=True)
        else:
            self.delete()

        # Set as dirty
        self.entity.dirty = False

    @property
    def entity(self) -> 'kge.Canvas':
        return self._entity

    @entity.setter
    def entity(self, e: 'kge.Canvas'):
        if e is not None and not isinstance(e, kge.Canvas):
            raise TypeError(f"Should be a canvas (kge.Canvas)")

        # if e is not None and e != self._entity:

        # set entity
        self._entity = e

    def on_disable_entity(self, ev: events.DisableEntity, dispatch):
        """
        Disable elements if visible
        """
        self.delete()

    def on_enable_entity(self, ev: events.EnableEntity, dispatch):
        """
        Enable elements if visible
        TODO
        """

    def on_destroy_entity(self, ev: events.DestroyEntity, dispatch):
        """
        Delete sprite if entity is being deleted
        """
        if self._vlist is not None:
            self._vlist.delete()
            self._vlist = None
        if self._sprite is not None:
            self._sprite.delete()
            self._sprite = None

    def on_scene_stopped(self, ev: events.SceneStopped, dispatch):
        """
        Delete and destroy all elements if visible
        """
        super(CanvasRenderer, self).on_scene_stopped(ev, dispatch)
        self.delete()

    def delete(self, redraw: bool = False):
        for e in self.entity.elements:  # type: UIElement
            e.delete()
            if redraw:
                e.append_to_render_list()
