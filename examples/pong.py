import logging
import time

import math
import random

import kge
from frame_counter import FrameCounter
from kge import *
from camera_controller import CameraController
from move_mixin import MoveMixin


class PlayerController(MoveMixin):
    UP_KEY = Keys.Z
    DOWN_KEY = Keys.S
    LEFT_KEY = Keys.Q
    RIGHT_KEY = Keys.D
    speed = 7


class PlayerController2(MoveMixin):
    UP_KEY = Keys.NumpadEight
    DOWN_KEY = Keys.NumpadTwo
    LEFT_KEY = Keys.NumpadFour
    RIGHT_KEY = Keys.NumpadSix
    speed = 7


class Player(Sprite):
    MAX_POINTS = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = Square(WHITE)
        self.transform.scale = Vector(1 / 2, 2)
        self.rb = RigidBody(RigidBodyType.KINEMATIC)
        self.rb.gravity_scale = 0
        self.rb.inertia = 5
        self.rb.entity = self
        self.score = 0

    def on_init(self, ev: events.Init, _):
        bounds = (
            ev.scene.Top - self.transform.scale.y / 2,
            ev.scene.Bottom + self.transform.scale.y / 2,
            ev.scene.Left + self.transform.scale.x / 2,
            ev.scene.Right - self.transform.scale.x / 2,
        )
        self.addComponent("col", BoxCollider(bounciness=1))
        self.addComponent("rb", self.rb)

        if self.tag == "Player One":
            self.addComponent("move", PlayerController(*(bounds)))
        else:
            self.addComponent("move", PlayerController2(*(bounds)))


YELLOW = (255, 255, 0, 255)
RADIUS = 1 / 5
MAX_BALL_SPEED = 10


class Ball(Sprite):

    def __init__(self, vel: Vector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = Circle(YELLOW, radius=RADIUS)
        self.transform.scale = Vector(RADIUS * 2, RADIUS * 2)
        self.rb = RigidBody()
        self.rb.velocity = vel
        self.rb.gravity_scale = 0

    def on_init(self, ev: events.Init, _):
        self.addComponent("col", CircleCollider(bounciness=1))
        self.addComponent("rb", self.rb)

    def on_fixed_update(self, ev, _):
        vx, vy = self.rb.velocity
        # Keep Ball for going too fast
        if abs(vx) > MAX_BALL_SPEED:
            vx = math.copysign(MAX_BALL_SPEED, vx)
        if abs(vy) > MAX_BALL_SPEED:
            vy = math.copysign(MAX_BALL_SPEED, vy)

        self.rb.velocity = Vector(vx, vy)


class Wall(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transform.scale = Vector(20, 1)
        # self.image = Square(BLACK)
        self.rb = RigidBody(RigidBodyType.DYNAMIC)
        self.rb.gravity_scale = 0

    def on_init(self, ev: events.Init, _):
        self.addComponent("col", BoxCollider())
        # self.addComponent("rb", self.rb)


class Goal(Sprite):
    def __init__(self, player_tag: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_tag = player_tag
        self.transform.scale = Vector(1, 20)
        # self.image = Square(BLACK)

    def on_init(self, ev: events.Init, _):
        self.addComponent("col", BoxCollider(isSensor=True))
    #
    # def on_update(self, ev: events.Update, _):
    #     players = list(ev.scene.get(kind=Player))
    #
    #
    #     hud = ""
    #     for player in players:
    #         hud = f'{hud}{player} {player.score} '
    #
    #     print(hud)

    def on_collision_enter(self, ev: physics_events.CollisionEnter, _):
        if isinstance(ev.collider.entity, Ball):
            player = list(ev.scene.get(tag=self.player_tag))

            # print("Ball Hit", player, self.player_tag)

            if player:
                p = player[0]  # type: Player
                p.score += 1
                ev.collider.entity.is_active = False
                ev.collider.entity.destroy()

                # print(p, "Goals !")

                ev.scene.addAll((Ball(name="Ball", vel=Vector(10, random.choice([-1, 1]) )), Vector(0, 0)),
                 )

def setup(scene: "Scene"):
    scene.main_camera.addComponent("controller", CameraController())
    scene.display_fps = True

    p1 = Player("player One", tag="Player One")
    p2 = Player("player Two", tag="Player Two")
    scene.addAll((p1, Vector(-7, 0)),
                 (p2, Vector(7, 0)),
                 (Ball(name="Ball", vel=Vector(10, random.choice([-1, 1]) )), Vector(0, 0)),
                 )

    scene.add(Wall(name="Wall Up"), position=Vector(0, 6))
    scene.add(Wall(name="Wall Down"), position=Vector(0, -6))
    scene.add(Goal(name="Goal Left", player_tag=p2.tag), position=Vector(-8, 0))
    scene.add(Goal(name="Goal Right", player_tag=p1.tag), position=Vector(8, 0))
    scene.add(FrameCounter(), position=Vector.Zero())


if __name__ == '__main__':
    kge.run(setup,
            title="PONG !",
            log_level=logging.INFO)
