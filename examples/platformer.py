from camera_controller import CameraController
import logging

import math

import kge
from frame_counter import FrameCounter
from kge import *
from kge import events, physics_events
# from kge_v1 import *
# from kge_v1.core.constants import RED
# from kge_v1.core.events import Update, MouseMotion, KeyDown, StopScene
# from kge_v1.physics.events import CollisionEnter
from move_mixin import MoveMixin


class FollowPlayer(Component):
    def on_late_update(self, ev: events.LateUpdate, _):
        players = list(ev.scene.get(kind=Player))

        if len(players) > 0:
            player = players[0]
            self.entity.position = Vector(
                player.position.x, self.entity.position.y)


class Bg(Sprite):
    def __init__(self):
        super().__init__("Background")
        self.image = Image("assets/bg_effect.png")
        self.transform.scale = Vector(1000 / 640, 700 / 480)
        self.layer = -1
        self.addComponent("follow", FollowPlayer(self))


class DestructionLayer(Sprite):
    def on_init(self, ev, _):
        self.transform.scale = Vector(50, 1)
        self.addComponent("d", BoxCollider(isSensor=False))

    def on_collision_enter(self, ev: physics_events.CollisionEnter, _):
        print(ev.collider.entity)
        # ev.collider.entity.destroy()


class Ground(Sprite):
    def __init__(self):
        super().__init__()
        # self.image = OutLinedSquare(RED)
        self.image = Image("assets/ground.png")


    def on_init(self, ev, _):
        self.addComponent("collider", BoxCollider(
            box=Vector(1, 1), friction=.01))

    # def on_update(self, ev, _):
    #     print(f"Ground Box : {self.position}")


class GroundRight(Sprite):
    def __init__(self):
        super().__init__()
        self.image = Image("assets/ground_right.png")

    def on_init(self, ev, _):
        self.addComponent("collider", BoxCollider(friction=.1))


class GroundLeft(Sprite):
    def __init__(self):
        super().__init__()
        # self.image = OutLinedSquare(RED)
        self.image = Image("assets/ground_left.png")

    def on_init(self, ev, _):
        self.addComponent("collider", BoxCollider(friction=.1))


class Box(Sprite):
    target = Vector(0, 0)
    speed = 2

    def __init__(self):
        super().__init__("Box")
        self.image = Image("assets/box.png")
        self.shape = Triangle(RED)
        self.layer = 1
        self.rb = RigidBody(body_type=RigidBodyType.DYNAMIC)
        self.rb.angular_velocity = .5
        self.rb.fixed_rotation = False
        # self.transform.angle = 45

    # def on_mouse_motion(self, ev: MouseMotion, _):
    #     """
    #     on mouse motion
    #     """
    #     self.target = ev.position
    #
    # def on_update(self, ev, _):
    #     # print(self.target)
    #     intent_vector = self.target - self.position
    #     if intent_vector:
    #         # self.position += intent_vector.scale(self.speed * ev.delta_time)
    #         # print(math.degrees(math.atan2(intent_vector.y, intent_vector.x)) - 90)
    #         self.transform.angle = math.degrees(math.atan2(intent_vector.y, intent_vector.x)) - 90

    def on_init(self, ev, _):
        pass
        self.addComponent("rb", self.rb)
        self.addComponent("col", BoxCollider(friction=10))


class PlayerController(MoveMixin):
    UP_KEY = Keys.Z
    DOWN_KEY = Keys.S
    LEFT_KEY = Keys.Q
    RIGHT_KEY = Keys.D
    speed = 7
    move_flexibility = Vector(1, 0)
    canJump = True
    jump_speed = 50


class Player(Sprite):
    def __init__(self):
        super().__init__(None, "Player")
        # self.image = OutLinedSquare(GREEN)  #
        self.image = Image("assets/player_stand.png")
        self.layer = 1
        self.rb = RigidBody()
        self.rb.fixed_rotation = True
        self.rb.gravity_scale = 1
        self._facingR = True
        self.controller = PlayerController()

    def on_init(self, ev, _):
        self.addComponent("move", self.controller)
        self.addComponent("rb", self.rb)
        self.addComponent("box", BoxCollider(
            box=Vector(.75, .75),
        ))

    def flip(self):
        self._facingR = not self._facingR
        self.flipX()

    def on_fixed_update(self, ev, _):
        physics = ServiceProvider.getPhysics()

        hit = physics.ray_cast(self.position, Vector.Down(), .6)
        # print(hit.collider)
        self.controller.on_ground = hit.collider is not None


    # def on_update(self, ev, _):
    #     horiz = int(self.rb.velocity.x)
    #     vert = int(self.rb.velocity.y)
    #
    #     if horiz != 0:
    #         if (horiz > 0 and not self._facingR) or (horiz < 0 and self._facingR):
    #             self.flip()
    #         # self.image = self._im2
    #     else:
    #         pass
    #         # self.image = self._im1
    #
    #     if vert > 0:
    #         pass
    #         # self.image = self._im3


def setup(scene: Scene):
    scene.background_color = BLUE
    # Set layer
    scene.setLayer(0, "Background")
    scene.setLayer(1, "Foreground")

    # Add component to main camera
    scene.display_fps = True
    scene.main_camera.addComponent("follow",
                                   # FollowPlayer())
                                   CameraController(None))

    # Add entities
    scene.add(Player(), position=Vector(0, -2), layer="Foreground")
    scene.add(Box(), position=Vector(2, 2), layer="Foreground")
    # scene.add(DestructionLayer(), position=Vector(0, -7), layer="Foreground")
    scene.add(Bg(), position=Vector.Zero(), layer="Background")
    scene.add(FrameCounter(), position=Vector.Zero())

    print(dir(CameraController()))

    # Add Ground tiles
    for i in range(-50, 50):
        # if i == -10:
        #     scene.add(GroundLeft(), position=Vector(i, -5), layer="Foreground")
        #
        # elif i == 19:
        #     scene.add(GroundRight(), position=Vector(
        #         i, -5), layer="Foreground")
        # else:
            scene.add(Ground(), position=Vector(i, -5), layer="Foreground")


if __name__ == '__main__':
    kge.run(setup, log_level=logging.INFO)
