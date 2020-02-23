from typing import Type, Union, List

import pyglet

import kge
from kge.core import events
from kge.core.service import Service
from kge.core.system import System


class EntityManager(System):
    """
    The system that manages entities
    """

    def set_entities(self, dt):
        """
        Disable entities if not in camera sight
        """
        scene = self.engine.current_scene
        for e in scene.all:
            if not scene.main_camera.in_frame(e):
                if e.is_active:
                    e.is_active = False
            else:
                if not e.is_active:
                    e.is_active = True


    def __enter__(self):
        pyglet.clock.schedule_interval(self.set_entities, 1 / 60)

    # def on_scene_started(self, event: events.SceneStarted, dispatch):
    #     print(event.scene.all)

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
        Type['kge.Component'], "kge.Component", List[Union[Type['kge.Component'], "kge.Component"]]],
                                     added: bool):
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

    def add_component(self, e: "kge.Entity", c: Union[Type["kge.Component"], "kge.Component"], key: str):
        """
        Add a component to an entity
        """
        if self._dispatch:
            ev = events.AddComponent(
                entity=e,
                component=c,
                key=key
            )
            ev.onlyEntity = e
            self._dispatch(ev, immediate=True)

    def remove_component(self, e: "kge.Entity", c: Union[Type["kge.Component"], "kge.Component", str]):
        """
        Remove a component to an entity
        """
        if self._dispatch:
            ev = events.RemoveComponent(
                entity=e,
                kind=c,
            )
            ev.onlyEntity = e
            self._dispatch(ev, immediate=True)


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
        Type['kge.Component'], "kge.Component", List[Union[Type['kge.Component'], "kge.Component"]]],
                                     added: bool):
        self._system_instance.dispatch_component_operation(e, c, added)

    def add_component(self, e: "kge.Entity", c: Union[Type["kge.Component"], "kge.Component"], key: str):
        self._system_instance.add_component(e, c, key)

    def remove_component(self, e: "kge.Entity", kind: Union[Type["kge.Component"], "kge.Component", str]):
        self._system_instance.remove_component(e, kind)
