from typing import Callable

import kge
from kge.core import events
from kge.core.component_system import ComponentSystem
from kge.graphics.animator import Animator


class AnimSystem(ComponentSystem):
    """
    The system that handles animations
    """

    def __init__(self, **_, ):
        super().__init__(**_)
        self.components_supported = [Animator]

    def on_update(self, ev: events.Update, dispatch: Callable[[events.Event], None]):
        """
        Animate by update
        TODO : TO CHANGE ?
        """
        if ev.scene.rendered:
            # scene = ev.scene
            # FIXME : REALLY NOT PERFORMANT !!!
            # anim_e = set(scene.entity_layers(kge.Entity, filter_set=self._entities, renderable=False))
            anim_e = self._components

            for animator in anim_e: # type: Animator
                # animator = e.getComponent(kind=Animator)
                animator.update(dispatch)
