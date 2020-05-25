from typing import Type

from kge.core.system import System

class ServicesMeta(type):
    def __getattribute__(self, item):
        obj = super().__getattribute__(item)
        if type(obj) is property:
            return obj.__get__(self, item)
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        obj = self.__dict__.get(key)
        if type(obj) is property:
            return obj.__set__(self, value)
        return super().__setattr__(key, value)

class Service(metaclass=ServicesMeta):
    system_class: Type[System]
    _system_instance: System = None
    instance: "Service" = None

    @classmethod
    def createInstance(cls, system_attached: System):
        if cls.instance is None:
            cls.instance = cls(system_attached)

        return cls.instance

    def __init__(self, instance: System):
       type(self)._system_instance = instance

if __name__ == '__main__':
    s = Service.createInstance(System())
    # print(Service.full,)
    # print(s.full)
    # class meta(type):
    #     def __getattribute__(self, item):
    #         print(self, item)
    #         return "I am a dork"
    #
    #     def __setattr__(self, key, value):
    #         print(self, key, value)
    #
    # class b(metaclass=meta):
    #     pass
    #
    # class c(b):
    #     pass
    #
    # print(b.hi)
    # b.hi = "Fredkiss"
    # print(c.foo)
    #



