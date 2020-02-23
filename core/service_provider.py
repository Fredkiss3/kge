from typing import Type, TypeVar

from kge.graphics.renderer import WindowService
from kge.inputs.input_manager import InputService
from kge.physics.physics_manager import Physics
from kge.audio.audio_manager import Audio
from kge.core.entity_manager import EntityManagerService
from kge.core.service import Service

T = TypeVar("T")

class ServiceProvider(object):
    """
    Class for providing services to users
    """
    services = {}

    @classmethod
    def getPhysics(cls) -> Physics:
        return cls.getService(Physics)

    @classmethod
    def getAudio(cls) -> Audio:
        return cls.getService(Audio)

    @classmethod
    def getEntityManager(cls) -> EntityManagerService:
        return cls.getService(EntityManagerService)

    @classmethod
    def getInputs(cls) -> InputService:
        return cls.getService(InputService)

    @classmethod
    def getWindow(cls) -> WindowService:
        return cls.getService(WindowService)

    @classmethod
    def getService(cls, kind: Type[T]) -> T:
        """
        get a service
        """
        try:
            return cls.services[kind]
        except KeyError:
            raise KeyError(f"The service '{kind.__name__}' has not been provided.")

    @classmethod
    def provide(cls, service: Service):
        """
        Provide a service
        """
        cls.services[type(service)] = service
