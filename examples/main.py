import logging
import time

import kge
from kge import *
from kge.core.constants import RED, BLUE

from kge.physics.events import CollisionEnter, FixedUpdate


class Projectile(Sprite):
    def __init__(self, name=None, tag=None):
        super().__init__(name, tag)
        self.transform.scale = Vector(0.25, 0.25)
        self.image = Image("assets/projectile.png")

    def on_init(self, init_event, dispatch):
        self.rb = RigidBody(body_type=RigidBody.DYNAMIC)
        self.addComponent("rb", self.rb)
        self.addComponent("colliderEnemy",
                          BoxCollider(
                              box=Vector(.25, .25),
                              isSensor=True,
                          ))
        # self.rb.velocity = Vector(0, 3)

    def on_collision_enter(self, ev: CollisionEnter, _):
        if isinstance(ev.collider.entity, Target):
            self.destroy()

    def on_fixed_update(self, ev: FixedUpdate, _):
        if self.position.y > 10:
            self.destroy()
        else:
            self.rb.move_position(self.position + Vector(0, 3) * ev.fixed_delta_time)


class EnemyHealth(Component):
    damage = 5
    death_sound = Sound("assets/bomb.wav")

    def take_damage(self):
        self.health -= self.damage

        if self.health <= 0:
            # print(f"{self} is Dead {self.health}")
            self.health = 0
            self.is_dead = True

    def on_init(self, init_event, dispatch):
        # health
        self.health = 100
        self.is_dead = False

    def on_update(self, ev: events.Update, dispatch):
        if self.is_dead:
            print("My death !!")

            # Get Audio
            audio = ServiceProvider.getAudio()
            audio.play(self.death_sound)
            self.entity.destroy()

            self.is_dead = False


class Target(Sprite):
    """
    Enemy
    """

    death_snd = Sound("assets/bomb.wav")

    def __init__(self, name=None, tag=None):
        super().__init__(name, tag)
        self.image = Image("assets/target.png")

    def on_init(self, init_event, dispatch):
        self.transform.scale = Vector(0.5, 0.5)
        # self.shape = Circle(120, 150, 180)
        # self.addComponent("health", EnemyHealth(self))
        self.addComponent("rb", RigidBody(body_type=RigidBody.STATIC))
        self.addComponent("colliderEnemy",
                          CircleCollider(
                              isSensor=True,
                          ))

    def on_collision_enter(self, ev: CollisionEnter, _):
        if isinstance(ev.collider.entity, Projectile):
            audio = ServiceProvider.getAudio()
            audio.play(self.death_snd)
            self.destroy()
    # def on_render(self, ev, _):
    #     if self.name == "enemy -1":
    #         print("I'm Being rendered")


class Ground(Sprite):
    def on_init(self, ev, _):
        self.transform.scale = Vector(40, 1)
        self.addComponent("col", BoxCollider())


class Movement(Component):
    direction = Vector(0, 0)

    def on_key_down(self, ev: events.KeyDown, _):
        if ev.key is Keys.Left:
            # _(events.TimeDilation(new_time_scale=ev.time_scale * .5))
            self.direction += Vector(-1, 0)
        elif ev.key is Keys.Right:
            self.direction += Vector(1, 0)
        # elif ev.key is Keys.Up:
        #     self.direction += Vector(0, 1)
        # elif ev.key is Keys.Down:
        #     self.direction += Vector(0, -1)

    def on_key_up(self, ev: events.KeyUp, _):
        if ev.key is Keys.Left:
            # _(events.TimeDilation(new_time_scale=ev.time_scale * .5))
            self.direction += Vector(1, 0)
        elif ev.key is Keys.Right:
            self.direction += Vector(-1, 0)
        # elif ev.key is Keys.Up:
        #     self.direction += Vector(0, -1)
        # elif ev.key is Keys.Down:
        #     self.direction += Vector(0, 1)

    def on_update(self, ev: events.Update, _):
        # inputs = ServiceLocator.getInputs()
        #
        # if inputs.get_key_down(Keys.Left):
        #     self.direction += Vector(-1, 0)
        # elif inputs.get_key_down(Keys.Right):
        #     self.direction += Vector(1, 0)
        # if inputs.get_key_down(Keys.Up):
        #     self.direction += Vector(0, 1)
        # if inputs.get_key_down(Keys.Down):
        #     self.direction += Vector(0, -1)

        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction

        rb = self.entity.getComponent(RigidBody)
        if rb is None:
            self.entity.position += Vector(direction * 5 * ev.delta_time)

    def on_fixed_update(self, ev: FixedUpdate, _):
        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction

        rb = self.entity.getComponent(RigidBody)
        if rb is not None:
            rb.move_position(self.entity.position + self.direction * 5 * ev.fixed_delta_time)
        # print(ev.scene.main_camera.position, self.entity.position)


class Player(Sprite):
    """
    a player
    """
    speed = 1
    target1 = Vector(0, 0)
    target2 = Vector(10, 0)
    rb = RigidBody()
    col = BoxCollider(
        box=Vector(.5, .25), friction=2, bounciness=.3,  # isSensor=True
    )

    # _image = Image("assets/player.png")
    snd = Sound("assets/laser1.ogg")

    last_shoot = time.monotonic()
    time_lag = .5

    def on_key_down(self, ev: events.KeyDown, _):
        if ev.key is Keys.Space:
            self.shoot(ev.scene)

    def shoot(self, scene: kge.Scene):
        audio = ServiceProvider.getAudio()
        audio.play(self.snd)
        scene.add(Projectile(), position=Vector(self.position + Vector(0, .5)))

    def on_init(self, ev: events.Event, _):
        # self.shape = Triangle(BLUE)
        self.image = Image("assets/player.png")
        self.transform.scale = Vector(1, 1)
        self.cur_target = self.target1
        self.direction = Vector(1, 0)
        # self.addComponent("col1", self.col)
        # self.addComponent("rigidbody", self.rb)

        self.transform.angle = 0
        # self.rb.angular_velocity = 1
        # self.col.active = True
        self.f = False

        self.addComponent("controller", Movement(self))

    # def on_fixed_update(self, ev: FixedUpdate, _):
    #     # ev.scene.main_camera.zoom = 2
    #     # print(self.transform.angle)
    #     physics = ServiceLocator.getPhysics()
    #     if not self.f:
    #         # self.rb.addForce(Vector(1, 0), True)
    #         self.f = True

    # hit = physics.ray_cast(self.position, Vector.Up(), 10)

    # if hit.collider:
    #     enemy = hit.collider.entity
    #     if isinstance(enemy, Enemy):
    #         health = enemy.getComponent(kind=EnemyHealth)  # type: EnemyHealth
    #
    #         if health:
    #             health.take_damage()
    # self.rb.move_position(self.position + self.direction * self.speed * ev.fixed_delta_time)


def setup(scene: Scene):
    scene.main_camera.addComponent("camController", Movement(scene.main_camera))
    scene.add(Player(), position=(0, 0))
    # scene.add(Player(45), position=(0, 2))
    # scene.add(Player(90), position=(0, 2))
    # scene.add(Ground(), position=(0, -1))
    # scene.add(Enemy(name="enemy"), position=(0, 7))

    for i in range(-10, 10):
        # print((i+5, 5))
        scene.add(Target(name=f"enemy {i + 1}"), (i + 2, 5))
        print(f"enemy {i + 1}", (i + 2, 5))


if __name__ == '__main__':
    kge.run(setup, log_level=logging.INFO)
