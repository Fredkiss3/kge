from typing import Type, TypeVar

from kge.core.system import System

from kge.graphics.renderer import Window
from kge.inputs.input_manager import Inputs
from kge.physics.physics_manager import Physics, DebugDraw
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
    def getInputs(cls) -> Inputs:
        return cls.getService(Inputs)

    @classmethod
    def getWindow(cls) -> Window:
        return cls.getService(Window)

    @classmethod
    def getDebug(cls) -> DebugDraw:
        return cls.getService(DebugDraw)

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
    def provide(cls, service: Type[Service], system: System):
        """
        Provide a service
        """
        service = service.createInstance(system)
        cls.services[type(service)] = service
