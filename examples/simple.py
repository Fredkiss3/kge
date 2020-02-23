from camera_controller import CameraController
import logging

import kge
from frame_counter import FrameCounter
from kge import *
from kge import events


class FollowPlayer(Component):
    def on_late_update(self, ev: events.LateUpdate, _):
        players = list(ev.scene.get(kind=Player))

        if len(players) > 0:
            player = players[0]
            self.entity.position = Vector(
                player.position.x, -player.position.y) + Vector(1, -1) * 3


class PlayerController(Component):
    def on_update(self, ev: events.Update, _):
        inputs = ServiceProvider.getInputs()

        direction = Vector.Zero()
        if inputs.get_key_down(Keys.Right):
            direction += Vector.Right()
        if inputs.get_key_down(Keys.Left):
            direction += Vector.Left()
        if inputs.get_key_down(Keys.Up):
            direction += Vector.Down()
        if inputs.get_key_down(Keys.Down):
            direction += Vector.Up()

        self.entity.position += direction * 5 * ev.delta_time


class Player(Sprite):
    def __init__(self, image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rb = RigidBody(RigidBodyType.DYNAMIC)
        self.rb.velocity = Vector(1, 0)
        self.transform.scale = Vector(1, 1)
        self.transform.angle = 45
        # self.image = Image(image)
        # self.image = OutlinedCircle(BLUE)

    def on_init(self, ev: events.Init, _):
        self.addComponent("rb1", self.rb)
        # self.addComponent("collider", CircleCollider(bounciness=1, ))
        self.addComponent("collider2", BoxCollider(
            bounciness=1, box=Vector(.75, .75)))


class Spike(Sprite):

    def __init__(self):
        super().__init__()
        # self.transform.scale = Vector(1, .5)
        self.image = Image("assets/box.png")  # Triangle(GREEN)

    def on_init(self, ev, _):
        self.addComponent("collider", BoxCollider())


class Ground(Sprite):
    rb = RigidBody(body_type=RigidBodyType.STATIC)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transform.scale = Vector(20, 2)
        self.addComponent("rb", self.rb)
        self.addComponent("collider", BoxCollider(friction=1))


def setup(scene: "kge.Scene"):
    scene.main_camera.addComponent("Controller", CameraController(None))
    scene.display_fps = True
    # Set layers
    scene.setLayer(1, "Ground")
    scene.setLayer(2, "Playground")
    scene.setLayer(0, "Background")

    scene.add(Player(name="Player One", image="assets/player_stand.png"),
              position=Vector(0, 3.5), layer="Playground")
    scene.add(Player(name="Player Two", image="assets/player2_stand.png"),
              position=Vector(0, 1), layer="Playground")

    for i in range(-10, 10):
        scene.add(Spike(), position=Vector(i, -.75), layer="Playground")

    # scene.add(Ground(name="Ground"), position=Vector(0, -2), layer="Ground")
    scene.add(FrameCounter(), position=Vector.Zero())


if __name__ == '__main__':
    kge.run(setup,
            log_level=logging.INFO
            )
