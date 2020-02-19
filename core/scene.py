from collections.abc import Collection
from collections import defaultdict
from copy import deepcopy
from typing import Iterator, Type, Callable, Sequence, Tuple, Union, TypeVar

import kge
from kge import ServiceProvider
from kge.core import events
from kge.core.camera import Camera
from kge.core.constants import BLACK, DEFAULT_RESOLUTION, DEFAULT_PIXEL_RATIO, RED
from kge.core.entity import BaseEntity
from kge.core.eventlib import EventMixin
from kge.utils.vector import Vector
from collections import OrderedDict

# Anything
T = TypeVar("T")


class EntityCollection(Collection):
    """A container for entities."""

    def __init__(self):
        self._all = set()
        self._kinds = defaultdict(set)
        self._tags = defaultdict(set)

    def __contains__(self, item: BaseEntity) -> bool:
        return item in self._all

    def __iter__(self) -> Iterator[BaseEntity]:
        return (x for x in list(self._all) if x.is_active)

    def __len__(self) -> int:
        return len(self._all)

    @property
    def kinds(self):
        """
        Get all kinds

        :return:
        """
        return self._kinds

    @property
    def tags(self):
        """
        Get all tags

        :return:
        """
        return self._tags

    def add(self, entity: BaseEntity, tag: str = None) -> None:
        """
        Add an entity to the container.

        entity: An Entity. The item to be added.
        tag: A string. Value that can be used to
              retrieve a group containing the entity.

        Examples:
            container.add(MyObject())

            container.add(MyObject(), tag="red")
        """
        if tag is not None and not isinstance(tag, str):
            raise TypeError(
                "tag must be a string")
        self._all.add(entity)

        for kind in type(entity).mro():
            self._kinds[kind].add(entity)

        if tag is None:
            tag = entity.tag
        self._tags[tag].add(entity)

    def get(self, *, kind: Type[T] = None, tag: str = None, **_) -> Iterator[T]:
        """
        Get an iterator of objects by kind or tag.

        kind: Any Entity or a subclass of Entity. Pass to get a subset of contained items with the given
              type.
        tag: A string. Pass to get a subset of contained items with
             the given tag.

        Pass both kind and tag to get objects that are both that type and that
        tag.

        Examples:
            container.get(type=MyObject)

            container.get(tag="red")

            container.get(type=MyObject, tag="red")
        """
        if kind is None and tag is None:
            raise TypeError(
                "get() takes at least one keyword-only argument. 'kind' or 'tag'.")
        kinds = self._all
        tags = self._all
        if kind is not None:
            kinds = self._kinds[kind]
        if tag is not None:
            tags = self._tags[tag]
        return (x for x in kinds.intersection(tags))

    def remove(self, entity: BaseEntity) -> None:
        """
        Remove the given object from the container.

        entity: An Entity contained by container.

        Example:
            >>> scene1.remove(entity)
        """
        # print(self._all, self._kinds)
        if entity in self._all:
            self._all.remove(entity)
            for kind in type(entity).mro():
                self._kinds[kind].remove(entity)
            for s in self._tags.values():
                s.discard(entity)


class BaseScene(EventMixin, EntityCollection):
    """
    A scene : it represents a level in a game
    In sum, it is just a bunch of entities
    """
    nbItems = 0
    engine: "kge.Engine" = None
    resolution: Vector = Vector(*DEFAULT_RESOLUTION)
    pixel_ratio: int = DEFAULT_PIXEL_RATIO

    @classmethod
    def load(cls, new_scene: Union[Type["BaseScene"], "BaseScene"], **kwargs):
        """
        Load a new scene
        """
        if cls.engine is not None:
            cls.engine.dispatch(events.ReplaceScene(
                new_scene=new_scene, kwargs=kwargs), immediate=True)
        else:
            raise AttributeError(
                f"The scene provided ('{new_scene}') has no engine associated with it")

    @classmethod
    def pause(cls):
        """
        Pause the running scene
        """
        if cls.engine is not None:
            cls.engine.pause_scene()
        else:
            raise AttributeError(f"The engine has not been provied")

    @property
    def Top(self):
        return self.main_camera.frame_top

    @property
    def Bottom(self):
        return self.main_camera.frame_bottom

    @property
    def Left(self):
        return self.main_camera.frame_left

    @property
    def Right(self):
        return self.main_camera.frame_right

    def __init__(self, set_up: Callable = None, **kwargs):
        super(BaseScene, self).__init__()
        Scene.nbItems += 1

        self.name = f"Scene {self.nbItems}"

        # Main Camera
        self.main_camera = Camera(
            resolution=self.resolution, pixel_ratio=self.pixel_ratio, )
        self.background_color = BLACK  # type: Sequence[int]

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.layers = OrderedDict()
        for i in range(20):
            self.layers[i] = i

        # Display FPS
        self.display_fps = False

        # set_up is callable for setting up the scene
        if set_up is not None:
            set_up(self)

    def getLayer(self, layer: Union[int, str]):
        if layer in self.layers:
            return self.layers[layer]
        else:
            raise KeyError("This layer is not in scene")

    def setLayer(self, layer_number: int, layer_name: str):
        """
        Name a layer
        :param layer_number: the layer number starting with zero
        :param layer_name: the name you want to call this layer
        """
        if not isinstance(layer_name, str) and not isinstance(layer_number, int):
            raise TypeError(
                "Layer name should be a string, Layer number should be an integer")

        val = self.layers[layer_number]
        self.layers[layer_name] = val

    def __repr__(self):
        return self.name

    def add(self, entity: BaseEntity, position: Union[Tuple[float, float], Vector] = Vector.Zero(),
            layer: Union[int, str] = 0) -> None:
        """
        Add one entity in format :
            - (entity, position, layer)

        Usage :
            >>> scene1.add( player, Vector(1, 2), layer=1 )

        :param entity:
        :param position:
        :return:
        """
        # Set scene
        entity.scene = self

        # Set position
        entity.position = position

        # Set layer
        if isinstance(layer, (int, str)):
            entity.layer = self.getLayer(layer)
        else:
            raise TypeError("Layer must be integers or string")

        killer = ServiceProvider.getEntityManager()

        # Enable or disable entity
        if entity.is_active:
            killer.enable(entity)
        else:
            killer.disable(entity)

        super(BaseScene, self).add(entity, entity.tag)

    def addAll(self, *entities: Tuple[BaseEntity, Union[Tuple[float, float], Vector]]):
        """
        Add Many entities in the scene in one shot in format :
          - (entity, position)

        Usage :
        >>> scene1.addAll( (player, Vector(1,1)), (enemy, Vector(1,2)),  )

        :param entities:
        :return:
        """
        for entity, position in entities:
            entity.position = position
            super(BaseScene, self).add(entity)

    def entity_layers(self) -> Iterator:
        """
        Return an iterator of the contained Entities in ascending layer
        order and in frame.

        Sprites are part of a layer if they have a layer attribute equal to
        that layer value. Sprites without a layer attribute are considered
        layer 0.

        This function exists primarily to assist the Renderer subsystem,
        but will be left public for other creative uses.
        """
        return sorted(
            filter(lambda e: hasattr(e, "sprite_renderer")  # and self.main_camera.in_frame(e)
                   ,
                   self),
            # self,
            key=lambda s: getattr(s, "layer", 0)
        )


Scene = BaseScene

if __name__ == '__main__':
    import math

    # print(math.degrees(math.atan2(1, 1)))

    class Sprite(BaseEntity):
        pass

    scene1 = BaseScene()
    scene2 = BaseScene()

    # Scene.load(scene2)

    player = Sprite(name="Player")
    ground = Sprite(name="Ground", tag="ground")
    key = Sprite(name="key", tag="key")

    enemies = [
        (Sprite(name=f"enemy {i + 1}", tag="enemy", ), Vector(i + 5, 1)) for i in range(5)]

    scene1.addAll((player, (1, 1)), (ground, Vector(0, -7)),
                  *enemies, (key, (2, 1)))

    player.is_active = False
    # print(list(scene.get(kind=Enemy, tag="destroyer")))
    # print(list(scene.get(kind=Player)))
    # print(len(list(scene)))

    # for entity in scene:
    #     print(entity, entity.transform.position)

    # the player pick the key
    # key.parent = player
    # print(player.transform.position, key.transform.position)

    # player.transform.position -= (5, 1)
    # print(player.transform.position, key.transform.position)

    # the player drop the key
    # key.parent = None

    # player.transform.position += (50, 1)
    # print(player.transform.position, key.transform.position)

    # scene1.add(key, (1, 5))

    for entity in scene1.entity_layers():
        print(entity, entity._transform.position)

    print(deepcopy(scene1))
    # key.destroy()
    # scene.remove(key)

    # print(key)
    # print(len(list(scene)))

    # print([scene.main_camera])
