from collections import deque
# from enum import Enum, auto
from typing import Deque, Set, TypeVar

from dataclasses import dataclass

import kge
# from kge.core.component import BaseComponent
from kge.core.entity import BaseEntity
from kge.ui.button import Button
from kge.ui.canvas_renderer import CanvasRenderer
from kge.ui.ui_element import UIElement
from kge.utils.spatial_hash import SpatialHash, Box
from kge.utils.vector import Vector


@dataclass
class CanvasEvent(object):
    pass


@dataclass
class ClickUp(CanvasEvent):
    zone: 'Box'


@dataclass
class Hover(CanvasEvent):
    zone: 'Box'


@dataclass
class ClickDown(CanvasEvent):
    zone: 'Box'


@dataclass
class Clear(CanvasEvent):
    pass


T = TypeVar('T', bound=kge.Component)

class Canvas(BaseEntity):
    """
    A canvas is a panel that holds ui elements
    TODO : Implement order in canvas
    """
    _event_set: Deque[UIElement]
    _to_render: Deque[UIElement]
    fixed: bool
    elements: Set[UIElement]

    def __new__(cls, *args,
                name: str = None,
                tag: str = None,
                scale: Vector = Vector.Unit() * 10,
                **kwargs):
        # set the entity
        inst = super().__new__(cls, name=name, tag=tag)

        # Scale of the entity
        inst.scale = scale

        # Visibility
        inst.visible = True

        # renderer
        inst.renderer = CanvasRenderer(inst)

        # Set this attribute in order to fix the canvas position to be always on screen
        # Or to be part of the world
        inst.fixed = True

        # Spatial Hash for dispatching events to children
        inst._spatial_hash = SpatialHash(1)

        # navigable elements
        # TODO : Think of Navigation with keyboard
        inst._navigable_types = [Button]
        inst._selected_index = 0

        # elements to render
        inst._to_render = deque()

        # Add Canvas Renderer at the same time
        manager = kge.ServiceProvider.getEntityManager()
        manager.dispatch_component_operation(inst, inst.renderer, added=True)

        # hover list & Click list
        inst._event_set = deque()
        inst._elements = set()
        return inst

    @property
    def elements(self):
        return self._elements

    @property
    def position(self):
        return self._transform.position

    @position.setter
    def position(self, value: Vector):
        if self._transform.position != value:
            if self.scene is not None:
                self.scene.spatial_hash.remove(self._transform.position, Vector(self.size.width, self.size.height),
                                               self)
                self.scene.spatial_hash.add(value, Vector(self.size.width, self.size.height), self)
            self._transform.position = value

    @property
    def to_render(self):
        return self._to_render

    def add(self, element: UIElement, position: Vector = Vector.Zero()):
        """
        Add a ui element to the canvas
        :param element: the element to add
        :param position: position of the element relative to the canvas, Vector(0, 0) is the center of the canvas
        """

        # Add element only if it overlaps with canvas to prevent not rendering elements that are out of sight
        my_box = Box(self.position, self.scale)
        offset = self.position + position
        e_box = Box(offset, element.size)

        if my_box.overlaps(e_box):
            # Set Parent & Position
            element.parent = self
            element.position = position

            # Add element to spatial hash
            self.spatial_hash.add(position, element.size, element)
            self._elements.add(element)
        else:
            raise IndexError("Cannot add an element out of the canvas")

    def remove(self, element: UIElement):
        """
        Remove the element from self
        :param element: the element to remove
        """
        self.spatial_hash.remove(element.position, element.size, element)
        self._elements.remove(element)

    def dispatch(self, e: CanvasEvent):
        """
        Dispatch events to ui elements
        :param zone:
        :return:
        """
        if isinstance(e, Clear):
            # Hover off
            while self._event_set:
                ui = self._event_set.popleft()
                ui.set_normal()

        elif isinstance(e, Hover) or isinstance(e, ClickDown) or isinstance(e, ClickUp):
            zone = e.zone
            zone.center = zone.center - self.position

            elements = self.spatial_hash.search(zone.center, zone.size, *self._navigable_types)

            for ui in elements:  # type: UIElement
                e_box = Box(ui.position, ui.size)
                if e_box.overlaps(zone):
                    if isinstance(e, ClickDown):
                        ui.set_click()
                    else:
                        ui.set_hover()

                    if isinstance(e, ClickUp):
                        ui.dispatch_click_events()

                    if not ui in self._event_set:
                        self._event_set.append(ui)

    # def addComponent(self, component: T):
    #     """
    #     Cannot add a component
    #     """
    #     raise TypeError("Cannot add another component to the canvas")

    @property
    def spatial_hash(self):
        return self._spatial_hash

    def rehash(self):
        self._spatial_hash = SpatialHash(1)

    def __repr__(self):
        return f"{self.name} (Canvas)"
