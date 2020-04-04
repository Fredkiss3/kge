from typing import Type

from kge.core.system import System


class Service:
    system_class: Type[System]

    def __init__(self, instance: Type[System]):
        self._system_instance = instance
