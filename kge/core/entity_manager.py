from typing import Type, Union, List, Dict, Iterator

import kge
from kge.core import events
from kge.core.component import Component
from kge.core.service import Service
from kge.core.system import System
from kge.utils.coroutine import Coroutine


class EntityManager(System):
    """
    The system that help to dispatch entities' events to other systems
    """

    def __init__(self, **_):
        super().__init__(**_)
        # coroutines attached to each entity
        self.coroutines = {}  # type: Dict[kge.Entity, List[Coroutine]]

    def destroy(self, e: "kge.Entity"):
        if not e.destroyed:
            e.destroyed = True
            print("DESTROYING :", e)
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

    def remove_component(self, e: "kge.Entity", c: Union[Type["Component"], "Component", str]):
        """
        Remove a component to an entity
        """
        e.removeComponent(kind=c)

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
        entities = filter(lambda e: isinstance(e, kge.Entity),
                          ev.scene.registered_entities(ev))  # type: Iterator[kge.Entity]

        for e in entities:
            if self.engine.running:
                e.__fire_event__(ev, dispatch)
                if e.coroutines:
                    for c in e.coroutines:  # type: Coroutine
                        c.stop_loop()
            else:
                # Break if the engine has finished running
                break
        self.coroutines.clear()


class EntityManagerService(Service):
    system_class = EntityManager
    _system_instance: EntityManager

    @classmethod
    def destroy(self, e: "kge.Entity"):
        self._system_instance.destroy(e)

    @classmethod
    def enable(self, e: "kge.Entity"):
        self._system_instance.enable(e)

    @classmethod
    def disable(self, e: "kge.Entity"):
        self._system_instance.disable(e)

    @classmethod
    def dispatch_component_operation(self, e: "kge.Entity", c: Union[
        Type['Component'], "Component", List[Union[Type['Component'], "Component"]]],
                                     added: bool):
        self._system_instance.dispatch_component_operation(e, c, added)

    @classmethod
    def add_component(self, e: "kge.Entity", c: Union[Type["Component"], "Component"]):
        self._system_instance.add_component(e, c)

    @classmethod
    def remove_component(self, e: "kge.Entity", kind: Union[Type["Component"], "Component", str]):
        self._system_instance.remove_component(e, kind)

    @classmethod
    def addCoroutine(self, e: "kge.Entity", c: Coroutine):
        try:
            self._system_instance.coroutines[e].append(c)
        except KeyError:
            self._system_instance.coroutines[e] = [c]
