from typing import Union, Callable

from kge.core import events
from kge.core.events import Event
from kge.core.constants import DEFAULT_RESOLUTION, MAX_ZOOM, MIN_ZOOM, DEFAULT_PIXEL_RATIO
from kge.core.entity import Entity
from kge.utils.vector import Vector
from kge.utils.dotted_dict import DottedDict


class Camera(Entity):
    """
    A camera attached to a scene
    """

    def __init__(self, name="MainCamera", tag="MainCamera",
                 resolution: "Vector" = Vector(*DEFAULT_RESOLUTION),
                 pixel_ratio: int = DEFAULT_PIXEL_RATIO):
        """
        :param name: the name of the camera
        :param tag: the tag of the camera
        :param pixel_ratio: unit of conversion
            - Example :
                - in the game, if we set an entity a size of 1x1, it will be translated to 64x64 pixels
        """
        super().__init__(name, tag)
        self._zoom = 1.0
        self.resolution = DottedDict(width=resolution.x, height=resolution.y)
        self.pixel_ratio_original = pixel_ratio
        self.pixel_ratio = self.pixel_ratio_original * self._zoom

    def on_window_resized(self, ev: events.WindowResized, dispatch: Callable[[Event], None]):
        self.resolution = DottedDict(width=ev.new_size.x, height=ev.new_size.y)

    @property
    def zoom(self):
        """
        Zoom, can't be greater than MAX_ZOOM = 10
        and can't be lower than MIN_ZOOM = 1
        :return:
        """
        return self._zoom

    @zoom.setter
    def zoom(self, value: Union[float, int]):
        if isinstance(value, (float, int)):
            if MIN_ZOOM <= float(value) <= MAX_ZOOM:
                self._zoom = float(value)
                self.pixel_ratio = self.pixel_ratio_original * self._zoom
        else:
            raise TypeError("Zoom is a float or an int")

    @property
    def frame_top(self) -> float:
        """
        Frame top position in unit

        :return:
        """
        return self.position.y + self.half_height

    @property
    def frame_bottom(self) -> float:
        """
        Frame bottom position in unit

        :return:
        """
        return self.position.y - self.half_height

    @property
    def frame_left(self) -> float:
        """
        Frame left position in unit

        :return:
        """
        return self.position.x - self.half_width

    @property
    def frame_right(self) -> float:
        """
        Frame right position in unit

        :return:
        """
        return self.position.x + self.half_width

    @property
    def frame_height(self) -> float:
        """
        Frame Height in units

        :return:
        """
        return self.pixels_to_unit(self.resolution.height)

    @property
    def frame_width(self) -> float:
        """
        Frame Width in units

        :return:
        """
        return self.pixels_to_unit(self.resolution.width)

    @property
    def half_height(self) -> float:
        """
        Get half height of the frame in units

        :return:
        """
        return self.frame_height / 2

    @property
    def half_width(self) -> float:
        """
        Get half width of the frame in units

        :return: half width
        """
        return self.frame_width / 2

    def in_frame(self, entity: Entity) -> bool:
        """
        Is this entity in the screen ?
        This method is meant to be used with the renderer system in order to render
        only elements that are in camera sight.

        :param entity: the entity to check
        :return: True of the entity is in camera sight
        """
        # Minimum distances before the collision occurs
        min_dist_x = entity.size.width / 2 + self.half_width
        min_dist_y = entity.size.height / 2 + self.half_height

        # vector from the entity to the camera
        distVec = entity.position - self.position

        # depth of the collision
        xDepth = min_dist_x - abs(distVec.x)
        yDepth = min_dist_y + abs(distVec.y)

        if xDepth > 0 and yDepth > 0:
            return True

        return False

    def screen_to_world_point(self, point: Vector) -> Vector:
        """
        Get units coordinates of a pixel coordinates point in screen
        """
        # 1. Scale from pixels to game units
        scaled = self.pixels_to_unit(point)
        # 2. Reposition relative to frame edges
        return Vector(self.frame_left + scaled.x, scaled.y - self.frame_top)

    def world_to_screen_point(self, point: Vector) -> Vector:
        """
        Get real screen pixels coordinates of the point.
        Used to retrieve the position in which we should draw the point
        """

        # 1. Reposition based on frame edges
        vector = Vector(point.x - self.frame_left, self.frame_top + point.y)
        # 2. Scale from game units to pixels
        return Vector(self.unit_to_pixels(vector))

    def pixels_to_unit(self, pixels: Union[float, Vector]) -> Union[float, Vector]:
        """
        Convert pixels to unit in the world

        :return:
        """
        return pixels / self.pixel_ratio

    def unit_to_pixels(self, unit: Union[float, Vector]) -> Union[float, Vector]:
        """
        Convert a point to pixels

        :param unit:
        :return:
        """
        if isinstance(unit, float):
            return unit * self.pixel_ratio
        elif isinstance(unit, Vector):
            return Vector(unit * self.pixel_ratio)
        else:
            raise TypeError("unit must be either a float value or a vector")


if __name__ == '__main__':
    from kge.core.entity import Entity

    class Player(Entity):

        @property
        def size(self) -> DottedDict:
            return DottedDict(
                width=2, height=2
            )

    class Terrain(Entity):

        @property
        def size(self) -> DottedDict:
            return DottedDict(
                width=20, height=20
            )

    cam = Camera(resolution=Vector(640, 640))

    print(cam.position, cam.frame_left, cam.frame_right)
    # cam2 = cam.copy()
    player1 = Player(name="Player One")
    # player1.position = (-1, -1)
    # player2 = Player(name="Player Two")
    # player2.position = (1, 1)

    # print(cam.screen_to_world_point(Vector(1000, 700)))
    #
    # print(cam.world_to_screen_point(cam.position))
    # print(cam.world_to_screen_point(player1.position),
    #       cam.screen_to_world_point(cam.world_to_screen_point(player1.position)))
    # print(cam.world_to_screen_point(player2.position),
    #       cam.screen_to_world_point(cam.world_to_screen_point(player2.position)))

    box = Terrain("Ground Box")
    player1.position = Vector.Zero()

    print(cam.in_frame(box), box.left, box.right)
    print(cam.in_frame(player1), player1.left, player1.right)

    player1.position = Vector(-5, 0)
    print(cam.in_frame(player1), player1.left, player1.right)

    player1.position = Vector(-6, 0)
    print(cam.in_frame(player1), player1.left, player1.right)

    # player1.position = Vector.Right()
    # print(cam.world_to_screen_point(player1.position))
    # cam.position = Vector.Right()
    # print(cam.world_to_screen_point(player1.position))

    # print(cam.in_viewport(player1), cam.in_viewport(player2))
    # print(cam.offset(player1.position), player1.position)

    # print(cam.resolution)
    # print(cam.offset(cam.position))
    # print(cam.world_to_screen_point(player1.position))

    # cam.position += (4.8126, 0)
    # player1.position += (0, 0)

    # print(cam.offset(player1.position), player1.position)
    # print(cam.offset(cam.position))
    # print(cam.world_to_screen_point(player1.position))

    # print(cam.position, cam.frame_left, cam.frame_right)
    # print(cam.in_viewport(player1), cam.in_viewport(player2))

    # player.position = Vector(-1, 0)
    # # print(player.transform.position)
    # unit = cam.offset(player.position)
    # print(cam.world_to_screen_point(unit) == cam.world_to_screen_point(player.position))
    #
    # cam.position += Vector(-2, 0)
    # # print(player.transform.position)
    # unit = cam.offset(player.position)
    #
    # print(cam2.world_to_screen_point(unit) == cam.world_to_screen_point(player.position))

    # v = c.transform.position + Vector(*DEFAULT_RESOLUTION)
    # point_in_pixels = c.screen_to_world_point(v)
    #
    # print(point_in_pixels)
    #
    # point_in_units = c.world_to_screen_point(point_in_pixels)
    #
    # print(point_in_units)
