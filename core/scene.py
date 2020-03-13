from collections.abc import Collection
from collections import defaultdict
from copy import deepcopy
from typing import Iterator, Type, Callable, Sequence, Tuple, Union, TypeVar, Set, Dict, List

import kge
from kge import ServiceProvider
from kge.core import events
from kge.core.camera import Camera
from kge.core.constants import BLACK, DEFAULT_RESOLUTION, DEFAULT_PIXEL_RATIO, MAX_LAYERS
from kge.core.entity import BaseEntity
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
    def all(self) -> Set[BaseEntity]:
        """
        Get all entities
        """
        return self._all

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


class BaseScene(EntityCollection):
    """
    A scene is a Level in the game.

    In order to

    """
    nbItems = 0
    engine: "kge.Engine" = None
    resolution: Vector = Vector(*DEFAULT_RESOLUTION)
    pixel_ratio: int = DEFAULT_PIXEL_RATIO

    @classmethod
    def load(cls, setup: Callable[["BaseScene"], None]=None, **kwargs):
        """
        Load a new scene
        """
        new_scene = cls(setup)

        if cls.engine is not None:
            cls.engine.dispatch(events.ReplaceScene(
                new_scene=new_scene,
                kwargs=kwargs
            ), immediate=True)
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
        return self.main_camera.real_frame_top

    @property
    def Bottom(self):
        return self.main_camera.real_frame_bottom

    @property
    def Left(self):
        return self.main_camera.frame_left

    @property
    def Right(self):
        return self.main_camera.frame_right

    def __init__(self, set_up: Callable[["BaseScene"], None] = None, **kwargs):
        super(BaseScene, self).__init__()
        self._event_map = dict() # type: Dict[str, List[BaseEntity]]
        Scene.nbItems += 1

        self.name = f"Scene {self.nbItems}"

        # Main Camera
        self.main_camera = Camera(
            resolution=self.resolution, pixel_ratio=self.pixel_ratio, )
        self.background_color = BLACK  # type: Sequence[int]

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.layers = OrderedDict()
        for i in range(MAX_LAYERS):
            self.layers[i] = i

        # Display FPS
        self.display_fps = False

        # set_up is callable for setting up the scene
        if set_up is not None:
            set_up(self)

    def getLayer(self, layer: Union[int, str]):
        """
        Get a layer by its name or order,
        there are only 20 layers.
        """
        if layer in self.layers:
            return self.layers[layer]
        else:
            raise KeyError("This layer is not in scene")

    def setLayer(self, layer_number: int, layer_name: str):
        """
        Give a name to a layer
        :param layer_number: the layer number starting from 0 to 20
        :param layer_name: the name you want to call that layer
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
            >>> scene1.setLayer(1, "Foreground")
            >>> scene1.add( player, position=Vector(1, 2), layer="Foreground" )

        :param entity: the entity to add to the scene
        :param position: the position of the entity in the scene
        :param layer: the layer in which the entity should be
        :return:
        """
        # Set scene
        entity.scene = self

        # Set position
        entity.transform.position = position

        # Set layer
        if isinstance(layer, (int, str)):
            entity.is_active = True
            entity.layer = self.getLayer(layer)
        else:
            raise TypeError("Layer must be an int or str")

        manager = ServiceProvider.getEntityManager()
        # Enable or disable entity
        if entity.is_active:
            manager.enable(entity)
        else:
            manager.disable(entity)

        super(BaseScene, self).add(entity, entity.tag)
        # Initialize the entity
        entity.__fire_event__(events.Init(self), self.engine.dispatch)
        self.register_events(entity)

    def addAll(self, *entities: Tuple[BaseEntity, Union[Tuple[float, float], Vector], Union[str, int]]):
        """
        Add Many entities in the scene in one shot in format :
          - (entity, position, layer)

        Usage :
        >>> scene1.addAll( (player, Vector(1,1), "Foreground"), (enemy, Vector(1,2), 1),  )

        :param entities:
        :return:
        """
        for entity, position, layer in entities:
            self.add(entity, position, layer)

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
            filter(lambda e: hasattr(e, "sprite_renderer")
                   # and self.main_camera.in_frame(e)
                   ,
                   self),
            key=lambda s: getattr(s, "layer", 0)
        )

    def clear(self):
        """
        Remove all entities from the scene
        """
        self.all.clear()
        self.kinds.clear()
        self._event_map = dict()

    def registered_entities(self, event):
        """
        Return registered entities for event
        """
        try:
            return self._event_map[type(event).__name__]
        except KeyError:
            return []

    @property
    def registered_events(self):
        return self._event_map.keys()

    def remove(self, entity: BaseEntity) -> None:
        """
        Remove an entity, and its events
        """
        super(BaseScene, self).remove(entity)
        self.unregister_events(entity)

    def register_events(self, e: BaseEntity):
        """
        Map names of events to components which need the event
        """
        for attribute in dir(e):
            if attribute.startswith("on_") and callable(getattr(e, attribute)):
                name = snake_to_camel(attribute)
                try:
                    l = self._event_map[name]
                except KeyError:
                    self._event_map[name] = [e]
                else:
                    l.append(e)

    def unregister_events(self, e: BaseEntity):
        """
        Remove the component from event map
        """
        for k, v in self._event_map.items():
            if e in v:
                v.remove(e)

def snake_to_camel(meth_name: str):
    if not meth_name.startswith("on_") or (meth_name[-1] not in "azertyuiopqsdfghjklmwxcvbn"):
        return None
    else:
        event_name = meth_name[3:].split("_")
        event = ""
        for name in event_name:  # type: str
            if len(name.strip()) > 0:
                event += name.capitalize()
        return event

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
