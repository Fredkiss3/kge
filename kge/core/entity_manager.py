from typing import Type, Union, List, Dict, Callable

import pyglet

import kge
from kge.core import events
from kge.core.events import Event
from kge.core.service import Service
from kge.core.component import Component
from kge.core.system import System
from kge.utils.coroutines import Coroutine


class EntityManager(System):
    """
    The system that help to dispatch entities' events to other systems
    """

    def __init__(self, **_):
        super().__init__(**_)
        # coroutines attached to each entity
        self.coroutines = {} # type: Dict[kge.Entity, List[Coroutine]]

    def destroy(self, e: "kge.Entity"):
        if not e.destoyed:
            if self._dispatch:
                ev = events.DestroyEntity(
                    entity=e
                )
                ev.onlyEntity = e
                self._dispatch(ev, immediate=True)

    def disable(self, e: "kge.Entity"):
        if self._dispatch:
            ev = events.DisableEntity(
                entity=e
            )
            ev.onlyEntity = e
            self._dispatch(ev, immediate=True)

    def enable(self, e: "kge.Entity"):
        if self._dispatch:
            ev = events.EnableEntity(
                entity=e
            )
            ev.onlyEntity = e
            self._dispatch(ev, immediate=True)

    def dispatch_component_operation(self, e: "kge.Entity", c: Union[
        Type['Component'], "Component", List[Union[Type['Component'], "Component"]]],
                                     added: bool):
        """
        If component have been added, this dispatch "ComponentAdded" operation
        """
        if self._dispatch:
            if added:
                ev = events.ComponentAdded(
                    entity=e,
                    component=c,
                )
            else:
                ev = events.ComponentRemoved(
                    entity=e,
                    components=c,
                )
            ev.onlyEntity = e
            self._dispatch(ev, immediate=True)

    def add_component(self, e: "kge.Entity", c: Union[Type["Component"], "Component"]):
        """
        Add a component to an entity
        """
        e.addComponent(component=c)
        if self._dispatch:
            pass
            # ev = events.AddComponent(
            #     entity=e,
            #     component=c,
            # )
            # ev.onlyEntity = e
            # self._dispatch(ev, immediate=True)

    def remove_component(self, e: "kge.Entity", c: Union[Type["Component"], "Component", str]):
        """
        Remove a component to an entity
        """
        e.removeComponent(kind=c)
        if self._dispatch:
            pass
            # ev = events.RemoveComponent(
            #     entity=e,
            #     kind=c,
            # )
            # ev.onlyEntity = e
            # self._dispatch(ev, immediate=True)

    def on_destroy_entity(self, ev: events.DestroyEntity, dispatch):
        e = ev.onlyEntity

        if e.parent is not None:
            e.parent.children.remove(e)
            e.parent = None

        # Get attached Coroutines
        attached = self.coroutines.get(e, [])
        for coroutine in attached:
            coroutine.stop_loop()

        if len(attached) > 0:
            self.coroutines.pop(e)

        # Execute event when entity gets destroyed
        e.__fire_event__(ev, dispatch)

    def on_scene_stopped(self, ev: events.SceneStopped, dispatch):
        for e, lc in self.coroutines.items():
            for c in lc:
                c.stop_loop()


class EntityManagerService(Service):
    system_class = EntityManager
    _system_instance: EntityManager

    def destroy(self, e: "kge.Entity"):
        self._system_instance.destroy(e)

    def enable(self, e: "kge.Entity"):
        self._system_instance.enable(e)

    def disable(self, e: "kge.Entity"):
        self._system_instance.disable(e)

    def dispatch_component_operation(self, e: "kge.Entity", c: Union[
        Type['Component'], "Component", List[Union[Type['Component'], "Component"]]],
                                     added: bool):
        self._system_instance.dispatch_component_operation(e, c, added)

    def add_component(self, e: "kge.Entity", c: Union[Type["Component"], "Component"]):
        self._system_instance.add_component(e, c)

    def remove_component(self, e: "kge.Entity", kind: Union[Type["Component"], "Component", str]):
        self._system_instance.remove_component(e, kind)

    def addCoroutine(self, e: "kge.Entity", c: Coroutine):
        try:
            self._system_instance.coroutines[e].append(c)
        except KeyError:
            self._system_instance.coroutines[e] = [c]