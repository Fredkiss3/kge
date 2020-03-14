import logging
import math
import random
import time

import kge
from kge import *


class PlayerController(Behaviour):
    def __init__(self, BoundUp: float = float("inf"), BoundBottom: float = -float("inf")):
        super().__init__()
        # Bounds in order to not let the pad go too up or too down
        self.B_UP = BoundUp
        self.B_DN = BoundBottom
        self.speed = 7
        self.direction = Vector.Zero()

    def on_update(self, ev, _):
        inputs = ServiceProvider.getInputs()
        if inputs.get_key_down(Keys.Z):
            self.direction = Vector.Up()
        elif inputs.get_key_down(Keys.S):
            self.direction = Vector.Down()
        else:
            self.direction = Vector.Zero()

    def MovePlayer(self, direction: Vector):
        rb = self.entity.getComponent(RigidBody)
        if rb is not None:
            # The pad should not go over the bounds
            if self.B_DN < self.entity.position.y + direction.y < self.B_UP:
                rb.move_position(self.entity.position + direction)
            else:
                if not self.B_DN < self.entity.position.y + direction.y:
                    rb.move_position(Vector(self.entity.position.x, self.B_DN))
                elif not self.entity.position.y + direction.y < self.B_UP:
                    rb.move_position(Vector(self.entity.position.x, self.B_UP))

    def on_fixed_update(self, ev: events.FixedUpdate, _):
        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction

        # Move the player
        self.MovePlayer(direction * self.speed * ev.fixed_delta_time)


class AIController(Behaviour):
    """
    The controller of the A.I.
    """

    def __init__(self, BoundUp: float = float("inf"), BoundBottom: float = -float("inf")):
        super().__init__()
        # Bounds in order to not let the pad go too up or too down
        self.B_UP = BoundUp
        self.B_DN = BoundBottom

    def on_late_update(self, ev: events.LateUpdate, _):
        balls = list(ev.scene.get(kind=Ball))

        if balls:
            target = balls[0]

            # Get rigid body
            rb = self.entity.getComponent(RigidBody)
            if rb is not None:
                if target.position.y >= self.B_UP - self.entity.scale.y / 2:
                    rb.velocity = Vector.Zero()
                elif target.position.y <= self.B_DN + self.entity.scale.y / 2:
                    rb.velocity = Vector.Zero()
                else:
                    rb.move_position(Vector(self.entity.position.x, target.position.y))


class Player(Sprite):
    def __init__(self, name, tag, label: "Score"):
        super().__init__(name=name, tag=tag)
        # Add a Kinematic rigid body (This kind of body do not respond to forces and gravity)
        self.rb = RigidBody(RigidBodyType.KINEMATIC)

        # Score and label
        self.score = 0
        self.label = label

        # For collisions
        self.addComponent(BoxCollider(bounciness=1, box=Vector(
            24 / 64, 115 / 64
        )))
        self.addComponent(self.rb)
        if self.tag == "Player One":
            self.image = Image("assets/pad.png")
        else:
            self.image = Image("assets/pad2.png")

    def on_init(self, ev: events.Init, _):
        if self.tag == "Player One":
            bounds = (
                ev.scene.Top - (self.scale.y / 2 + 1 / 2),
                ev.scene.Bottom + (self.scale.y / 2 + 1 / 2),
            )
            self.addComponent(PlayerController(*(bounds)))
        else:
            bounds = (
                ev.scene.Top - self.transform.scale.y / 2 - .75,
                ev.scene.Bottom + self.transform.scale.y / 2 + .75,
            )
            self.addComponent(AIController(*(bounds)))


class Score(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_size = 15
        self.value = "0"


class Ball(Sprite):
    def __init__(self, vel: Vector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ball should not be too fast
        self.MAX_BALL_SPEED = 20

        # Wait before moving
        self.started_at = None
        self.time_to_wait = 1
        self.can_go = False

        # Velocity of the ball
        self.vel = vel

        # The image of the ball
        self.image = Image("assets/ball.png")

        # Physics components
        self.rb = RigidBody()  # Add a rigid body
        self.rb.gravity_scale = 0  # It should not be affected by gravity
        self.rb.velocity = Vector.Zero()  # Set velocity to zero to stop the ball for moving

        # This helps for responding to collisions
        self.addComponent(
            CircleCollider(
                bounciness=1,
                radius=1 / 6,
                center=Vector(-.03, 0)  # offset the center of the collider
                # from the center of the game object
            )
        )
        self.addComponent(self.rb)

    def on_update(self, ev, _):
        if self.rb.velocity == Vector.Zero() and not self.can_go:
            if self.started_at is None:
                self.started_at = time.monotonic()
                return

            # # The ball should wait a certain time before moving
            if time.monotonic() - self.started_at >= self.time_to_wait:
                self.can_go = True
                self.rb.velocity = self.vel

    def on_fixed_update(self, ev, _):
        if self.can_go:
            vx, vy = self.rb.velocity
            # Keep Ball for going too fast
            if abs(vx) > self.MAX_BALL_SPEED:
                vx = math.copysign(self.MAX_BALL_SPEED, vx)
            if abs(vy) > self.MAX_BALL_SPEED:
                vy = math.copysign(self.MAX_BALL_SPEED, vy)

            # Change the body velocity
            self.rb.velocity = Vector(vx, vy)


class Wall(Entity):
    """
    A wall, it is an invisible game object which the ball uses to bounce itself
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # st the scale of the entity to 20 in width and 1 in height
        self.scale = Vector(20, 1)

        # Physics components
        self.rb = RigidBody()
        self.rb.gravity_scale = 0  # No gravity
        self.addComponent(BoxCollider())  # Respond to collisions


class MusicPlayer(Behaviour):
    def on_init(self, ev, _):
        # Play sound
        snd = Sound("assets/bg_music.mp3")
        snd.play(1)


class Goal(Entity):
    """
    A Goal, it is an invisible game object which, the ball touches it,
    the score of the corresponding player gets incremented
    """

    def __init__(self, player_tag: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Which player tag correspond to the goal ?
        self.player_tag = player_tag

        self.scale = Vector(1, 20)  # the size of the goal is 1 in width and 20 in height
        self.addComponent(
            BoxCollider(
                isSensor=True  # for collisions, isSensor means that the ball should not bounce on it
            )
        )

    def on_collision_enter(self, ev: physics_events.CollisionEnter, _):
        # If hit by a ball
        if isinstance(ev.collider.entity, Ball):
            ball = ev.collider.entity
            # get player
            player = list(ev.scene.get(tag=self.player_tag))

            if player:
                p = player[0]  # type: Player
                # Increment player score
                p.score += 1
                p.label.value = str(p.score)  # Change label value
                ball.destroy()  # Destroy ball

                # Set random velocity for ball
                velx = random.choice([-10, 10])
                vely = random.randint(-5, 5)
                if vely == 0:
                    vely = random.choice([-5, 5])

                # Add ball to the scene
                ev.scene.add(Ball(name="Ball", vel=Vector(velx, vely)), layer="Fg")


def setup(scene: "Scene"):
    # Uncomment this line if you want to control the camera
    #   Use UP, DOWN, LEFT, RIGHT, arrow keys to move around
    #   And +, - to zoom in and zoom out
    # scene.main_camera.addComponent(CameraController())

    # Uncomment this to display the FPS
    # scene.display_fps = True
    scene.setLayer(0, "Bg")
    scene.setLayer(1, "Fg")

    # Background Image
    bg = Sprite(Image("assets/bg.jpg"))
    bg.addComponent(MusicPlayer())  # In order to play music

    # The score of the two players
    s1, s2 = Score(), Score()
    p1 = Player("player One", tag="Player One", label=s1)
    p2 = Player("AI", tag="Player Two", label=s2)

    # Add The players
    scene.addAll((p1, Vector(-7, 0), "Fg"),
                 (p2, Vector(7, 0), "Fg"))
    scene.add(Ball(name="Ball", vel=Vector(10, -4)), layer="Fg")
    scene.add(Wall(name="Wall Up"), position=Vector(0, 6))
    scene.add(Wall(name="Wall Down"), position=Vector(0, -6))
    scene.add(Goal(name="Goal Left", player_tag=p2.tag), position=Vector(-8, 0))
    scene.add(Goal(name="Goal Right", player_tag=p1.tag), position=Vector(8, 0))

    # Add score texts
    scene.add(s1, position=Vector(-1, 5), layer=15)
    scene.add(s2, position=Vector(1, 5), layer=15)
    scene.add(bg, layer="Bg")


if __name__ == '__main__':
    kge.run(setup,
            title="PONG !",
            # Set to debug if you want to see colliders and rigidBodies
            # log_level=logging.DEBUG,
            log_level=logging.INFO,
            )
