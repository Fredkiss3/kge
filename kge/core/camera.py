from typing import Union

from kge.core import events
from kge.core.constants import DEFAULT_RESOLUTION, MAX_ZOOM, MIN_ZOOM, DEFAULT_PIXEL_RATIO
from kge.core.entity import BaseEntity
from kge.physics.colliders import CameraCollider
from kge.physics.rigid_body import RigidBody, RigidBodyType
from kge.utils.dotted_dict import DottedDict
from kge.utils.vector import Vector


class Camera(BaseEntity):
    """
    A camera attached to a scene
    FIXME :
        - CANVAS POSITION & EVENT DISPATCHING SHOULD BE INDEPENDANT OF ZOOMING
        - FIX : CAMERA ZOOMING WITH RENDERERS
    """

    def __new__(cls, name="MainCamera", tag="MainCamera",
                resolution: "Vector" = Vector(*DEFAULT_RESOLUTION),
                pixel_ratio: int = DEFAULT_PIXEL_RATIO):
        """
       :param name: the name of the camera
       :param tag: the tag of the camera
       :param pixel_ratio: unit of conversion
           - Example :
               - in the game, if we set an entity a size of 1x1, it will be translated to 64x64 pixels
        """
        inst = super().__new__(cls, name=name, tag=tag)

        inst._zoom = 1.0
        inst._resolution = DottedDict(width=resolution.x, height=resolution.y)
        inst._pixel_ratio_original = pixel_ratio
        inst._pixel_ratio = inst._pixel_ratio_original * inst._zoom

        # FIXME : IS THERE A BETTER WAY OF HANDLING THIS ?
        inst.addComponents(
            RigidBody(body_type=RigidBodyType.KINEMATIC),
            CameraCollider(
                box=inst.pixels_to_unit(resolution) + Vector.Unit() / 2,
            ),
        )

        return inst

    def on_collision_enter(self, ev: events.CollisionEnter, dispatch):
        # Track Position of entities that enter in camera sight
        _ = lambda x: x
        _(ev.collider.entity.position)

    @property
    def resolution(self):
        """
        Get the resolution of the camera
        """
        return Vector(self._resolution.width, self._resolution.height)

    @resolution.setter
    def resolution(self, val: Vector):
        """
        Set the resolution of the camera
        """
        if not isinstance(val, Vector):
            raise TypeError("resolution should be a Vector")

        self._resolution = DottedDict(width=val.x, height=val.y)
        collider = self.getComponent(kind=CameraCollider)
        if collider:
            newBox = (self.pixels_to_unit(val) + Vector.Unit() / 2) * 1 / self.zoom
            collider.setBox(newBox)

    @property
    def pixel_ratio(self):
        """
        Get the pixel ratio of the camera
        """
        return self._pixel_ratio_original

    @property
    def position(self):
        return self._transform.position

    @position.setter
    def position(self, value: Vector):
        rb = self.getComponent(kind=RigidBody)
        if rb is not None:
            rb.velocity = Vector.Zero()
        if self._transform.position != value:
            # Set position of the body
            if rb is not None:
                rb.move_position(Vector(value.x, -value.y))

            self._transform.position = value

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
                if value != self._zoom:
                    # FIXME : TO REMOVE
                    # if self.scene is not None:
                    #     for e in self.scene:
                    #         e.dirty = True
                    #         e.debuggable = True
                    self._zoom = float(value)
                    self._pixel_ratio = self._pixel_ratio_original * self._zoom

                    collider = self.getComponent(kind=CameraCollider)
                    if collider:
                        newBox = (self.pixels_to_unit(self.resolution) + Vector.Unit() / 2) * 1 / self.zoom
                        collider.setBox(newBox)
        else:
            raise TypeError("Zoom should be a float or an int")

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
    def real_frame_top(self) -> float:
        """
        Real Frame top position in unit

        :return:
        """
        return -self.position.y + self.half_height

    @property
    def real_frame_bottom(self) -> float:
        """
        Real Frame bottom position in unit

        :return:
        """
        return -self.position.y - self.half_height

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
        return self.pixels_to_unit(self._resolution.height)

    @property
    def frame_width(self) -> float:
        """
        Frame Width in units

        :return:
        """
        return self.pixels_to_unit(self._resolution.width)

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

    def box_in_frame(self, point: Vector, size: Vector):
        """
        Check if a box is visible.
        You can use this method if you want to test sprites, rectangles and others
        """
        # Minimum distances before the collision occurs
        min_dist_x = size.x / 2 + self.half_width
        min_dist_y = size.y / 2 + self.half_height

        # vector from the entity to the camera
        distVec = point - Vector(self.position.x, -self.position.y)

        # depth of the collision
        # Difference between the Min Distance before a collision occurs
        # and the actual distance between camera and the box
        xDepth = min_dist_x - abs(distVec.x)
        yDepth = min_dist_y - abs(distVec.y)

        if xDepth > 0 and yDepth > 0:
            return True
        return False

    def in_frame(self, entity: BaseEntity) -> bool:
        """
        Is this entity in the screen ?
        This method is meant to be used with the renderer system in order to render
        only elements that are in camera sight.

        :param entity: the entity to check
        :return: True if the entity is in camera sight
        """
        # Minimum distances before the collision occurs
        min_dist_x = entity.size.width / 2 + self.half_width
        min_dist_y = entity.size.height / 2 + self.half_height

        # distance from camera to the entity
        distVec = entity.position - Vector(self.position.x, -self.position.y)

        # depth of the collision
        # Difference between the Min Distance before a collision occurs
        # and the actual distance between camera and entity
        xDepth = min_dist_x - abs(distVec.x)
        yDepth = min_dist_y - abs(distVec.y)

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

    # def on_window_resized(self, event: events.WindowResized, dispatch):
    #     self.resolution = DottedDict(width=event.new_size.x,height=event.new_size.y)

    def world_to_screen_point(self, point: Vector) -> Vector:
        """
        Get real screen pixels coordinates of the point.
        Used to retrieve the position in which we should draw the point
        """

        # 1. Reposition based on frame edges
        vector = Vector(point.x, point.y)
        # openGL offset 
        # GL_offset = self.unit_to_pixels(Vector(-self.position.x / 2, self.position.y / 2, ))
        GL_offset = Vector.Zero()
        # 2. Scale from game units to pixels
        return Vector(self.unit_to_pixels(vector) + GL_offset) * 1 / self._zoom

    def fixed_world_to_screen_point(self, point: Vector) -> Vector:
        """
        Get real screen pixels coordinates of the point.
        Used to retrieve the position in which we should draw the point
        FIXME : SET FOR UI
        """

        # 1. Reposition based on frame edges
        vector = Vector(point.x, point.y)
        # openGL offset 
        # GL_offset = self.unit_to_pixels(Vector(self.position.x, -self.position.y, ))
        GL_offset = Vector.Zero()

        # 2. Scale from game units to pixels
        return Vector(self.unit_to_pixels(vector) + GL_offset)

    def pixels_to_unit(self, pixels: Union[float, Vector]) -> Union[float, Vector]:
        """
        Convert pixels to unit in the world

        :return:
        """
        return pixels / self._pixel_ratio

    def unit_to_pixels(self, unit: Union[float, Vector]) -> Union[float, Vector]:
        """
        Convert a point to pixels

        :param unit:
        :return:
        """
        if isinstance(unit, (float, int)):
            return unit * self._pixel_ratio
        elif isinstance(unit, Vector):
            return Vector(unit * self._pixel_ratio)
        else:
            raise TypeError("unit must be either a float value or a vector")


if __name__ == '__main__':
    pass
