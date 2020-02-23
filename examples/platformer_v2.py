import logging

import math

import kge
from kge import *
from kge.core.constants import RED
from kge.core.events import Update, MouseMotion, KeyDown, StopScene
from kge.physics.events import CollisionEnter


class FollowPlayer(Component):
    def on_update(self, ev: Update, _):
        players = list(ev.scene.get(kind=Player))

        if len(players) > 0:
            player = players[0]
            self.entity.position = Vector(player.position.x, self.entity.position.y)


class Bg(Sprite):
    def __init__(self):
        super().__init__("Background")
        self.image = Image("assets/bg_effect.png")
        self.transform.scale = Vector(1000 / 640, 700 / 480)
        self.layer = -1
        self.addComponent("follow", FollowPlayer(self))


class DestructionLayer(Entity):
    def on_init(self, ev, _):
        self.transform.scale = Vector(50, 1)
        self.addComponent("d", BoxCollider(isSensor=True))

    def on_collision_enter(self, ev: CollisionEnter, _):
        print(ev.collider.entity)
        ev.collider.entity.destroy()


class Ground(Sprite):
    def __init__(self):
        super().__init__()
        self.image = Image("assets/ground.png")

    def on_init(self, ev, _):
        self.addComponent("collider", BoxCollider(box=Vector(1, 1), friction=.1))

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
        self.rb = RigidBody(body_type=RigidBody.DYNAMIC)
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


class MoveMixin(Component):
    """
    Move component
    """
    direction = Vector(0, 0)
    speed = 20
    max_speed = 7
    on_ground = False
    jump_speed = 3

    def Jump(self):
        rb = self.entity.getComponent(RigidBody)
        if rb is not None:
            rb.velocity = Vector(rb.velocity.x, 0)
            rb.add_force(Vector(Vector.Up() * self.jump_speed), True)

    def on_update(self, ev: events.Update, _):
        inputs = ServiceProvider.getInputs()

        if inputs.get_key_down(Keys.Space) and self.on_ground:
            self.Jump()

        if inputs.get_key_down(Keys.Left):
            self.direction = Vector.Left()
        elif inputs.get_key_down(Keys.Right):
            self.direction = Vector.Right()
        else:
            self.direction = Vector.Zero()

        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction

        rb = self.entity.getComponent(RigidBody)
        if rb is None:
            self.entity.position += Vector(direction * self.speed * ev.delta_time)

        # print(self.entity.position)
        physics = ServiceProvider.getPhysics()
        hit = physics.ray_cast(self.entity.position, Vector.Down(), 5)

        if hit.collider is not None:
            if isinstance(hit.collider.entity, (Ground, GroundLeft, GroundRight)):
                self.on_ground = True
            else:
                self.on_ground = False
        else:
            self.on_ground = False
        #
        # print(f"Player on Ground ? {self.on_ground}, {hit.point}")

    def MovePlayer(self, direction: Vector):
        rb = self.entity.getComponent(RigidBody)
        if rb is not None:
            rb.add_force(Vector(Vector.Right() * direction.x * self.speed))

            if abs(rb.velocity.x) > self.max_speed:
                # print("MAX SPEED  REACHED !!")
                rb.velocity = Vector(math.copysign(self.max_speed, rb.velocity.x), rb.velocity.y)
            # print(rb.velocity)

    def on_fixed_update(self, ev, _):
        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction

        rb = self.entity.getComponent(RigidBody)
        if rb is not None:
            # rb.move_position(self.entity.position + direction * 5 * ev.fixed_delta_time)
            self.MovePlayer(direction)


class Player(Sprite):
    def __init__(self):
        super().__init__("Player")
        self._im1 = Image("assets/player_stand.png")
        self._im2 = Image("assets/player_walk.png")
        self._im3 = Image("assets/player_jump.png")
        self.image = self._im1
        self.shape = Circle(RED)
        self.layer = 1
        self.rb = RigidBody()
        self.rb.fixed_rotation = True
        self.rb.gravity_scale = 1
        self._facingR = True
        # self.transform.scale = Vector(.75, .80)

    def on_init(self, ev, _):
        self.addComponent("move", MoveMixin(self))
        self.addComponent("rb", self.rb)
        self.addComponent("box", BoxCollider(box=Vector(.75, .80), ))

    def flip(self):
        self._facingR = not self._facingR
        self.flipX()

    def on_update(self, ev, _):
        horiz = int(self.rb.velocity.x)
        vert = int(self.rb.velocity.y)

        if horiz != 0:
            if (horiz > 0 and not self._facingR) or (horiz < 0 and self._facingR):
                self.flip()
            self.image = self._im2
        else:
            self.image = self._im1

        if vert > 0:
            self.image = self._im3


#
# class SceneManager(Component):
#     def on_key_down(self, ev: KeyDown, dispatch):
#         if ev.key is Keys.Space:
#             dispatch(StopScene(
#                 scene=ev.scene
#             ))
#         elif ev.key is Keys.P:
#             dispatch(StartScene())


def setup(scene: Scene):
    scene.main_camera.addComponent("follow", FollowPlayer(None))
    scene.add(Player(), position=Vector(0, -2))
    scene.add(Box(), position=Vector(2, 2))
    scene.add(DestructionLayer(), position=Vector(0, -7))
    scene.add(Bg(), position=Vector.Zero(), layer=-2)

    for i in range(-10, 20):
        if i == -10:
            scene.add(GroundLeft(), position=Vector(i, -5))

        elif i == 19:
            scene.add(GroundRight(), position=Vector(i, -5))

        else:
            scene.add(Ground(), position=Vector(i, -5))


if __name__ == '__main__':
    kge.run(setup, log_level=logging.INFO)
