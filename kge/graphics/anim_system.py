import pyglet

from kge.core import events
from kge.core.component_system import ComponentSystem
from kge.core.service import Service
from kge.graphics.animator import Animator


class AnimSystem(ComponentSystem):
    """
    The system that handles animations
    """

    # _pending: Set[Animator] = set()

    def __init__(self, **_, ):
        super().__init__(**_)
        self.components_supported = (Animator,)

    def on_destroy_entity(self, event: events.DestroyEntity, dispatch):
        """
        Unschedule animator after entity has been destroyed
        """
        for animator in event.entity.getComponents(kind=Animator):
            pyglet.clock.unschedule(animator.animate)
        super(AnimSystem, self).on_destroy_entity(event, dispatch)


class AnimService(Service):
    """
    Animation services
    FIXME: UNUSED
    """
    system_class = AnimSystem
    _system_instance: AnimSystem
    #
    # @classmethod
    # def append(cls, a: Animator):
    #     """
    #     Append animator to list of animators to start
    #     once the scene will be started
    #     """
    #     cls._system_instance.append(a)
