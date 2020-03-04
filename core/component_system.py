from kge.core import events
from kge.core.system import System
from kge.core.entity import Entity
from kge.core.component import Component
from typing import Union, Deque, Iterable, Optional, Callable, Any, List, Type, Dict, Iterator


class ComponentSystem(System):

    def __init__(self, engine=None, **_):
        super().__init__(engine, **_)

        # components types and components associated to this entity
        self.components_supported = []  # type: List[Type[Component]]
        self._components = []  # type: List[Component]

    def on_component_added(self, event: events.ComponentAdded, dispatch):
        component = event.component

        for type_ in self.components_supported:
            if isinstance(component, type_):
                self._components.append(component)

    def on_component_removed(self, event: events.ComponentRemoved, dispatch):
        components = event.components

        for component in components:
            if component in self._components:
                self._components.remove(component)

    def active_components(self) -> Iterator[Component]:
        """
        components that are active
        """
        return filter(lambda c: c.is_active or c.entity.is_active, self._components)
