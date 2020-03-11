from kge.core import events
from kge.core.system import System
from kge.core.component import Component
from typing import List, Type, Iterator, Dict


def snake_to_camel(meth_name: str):
    if not meth_name.startswith("on_") or (meth_name[-1] not in "azertyuiopqsdfghjklmwxcvbn"):
        return None
    else:
        event_name = meth_name[3:].split("_")
        event = ""
        for name in event_name:  # type: str
            if len(name.strip()) > 0:
                event += name.capitalize()
        return event


class ComponentSystem(System):

    def __init__(self, engine=None, **_):
        super().__init__(engine, **_)

        # components types and components associated to this entity
        self.components_supported = []  # type: List[Type[Component]]
        self._components = []  # type: List[Component]

        # the map between events and components in order to dispatch events
        # only to those which subscribed to the event
        self.event_map = dict()  # type: Dict[str, List[Component]]

    def on_component_added(self, event: events.ComponentAdded, dispatch):
        component = event.component

        for type_ in self.components_supported:
            if isinstance(component, type_):
                self._components.append(component)
                self.register_events(event.component)
                event.component.__fire_event__(events.Init(event.scene), dispatch)

    def register_events(self, b: Component):
        """
        Map names of events to components which need the event
        """
        for attribute in dir(b):
            if attribute.startswith("on_") and callable(getattr(b, attribute)):
                name = snake_to_camel(attribute)
                try:
                    l = self.event_map[name]
                except KeyError:
                    self.event_map[name] = [b]
                else:
                    l.append(b)

    def unregister_events(self, b: Component):
        """
        Remove the component from event map
        """
        for k, v in self.event_map.items():
            if b in v:
                v.remove(b)

    def on_component_removed(self, event: events.ComponentRemoved, dispatch):
        components = event.components

        for component in components:
            if component in self._components:
                self._components.remove(component)
                self.unregister_events(component)

    def active_components(self) -> Iterator[Component]:
        """
        components that are active
        """
        return filter(lambda c: c.is_active or c.entity.is_active, self._components)
