import math
import time
from typing import Optional

from kge import *


class MoveMixin(Behaviour):
    """
    Move component
    """
    direction = Vector(0, 0)
    fall_multiplier = 1
    speed = 10
    max_speed = 7
    jump_speed = 3
    canJump = False
    move_flexibility = Vector.Up()
    LEFT_KEY = Keys.Left
    RIGHT_KEY = Keys.Right
    DOWN_KEY = Keys.Down
    UP_KEY = Keys.Up
    drag = 0
    jump_delay = .25
    jump_timer = 0

    def __init__(self, BoundUp: float = float("inf"), BoundBottom: float = -float("inf"),
                 BoundLeft: float = -float("inf"), BoundRight: float = float("inf")):
        super().__init__()
        self.facingRight = True
        self.B_UP = BoundUp
        self.B_DN = BoundBottom
        self.B_LT = BoundLeft
        self.B_RT = BoundRight
        self.on_ground = False
        self.animator = None  # type: Optional[Animator]

    def Jump(self):
        rb = self.entity.getComponent(RigidBody)
        if rb is not None and rb.body_type == RigidBodyType.DYNAMIC:
            rb.velocity = Vector(rb.velocity.x, 0)
            rb.add_force(force=Vector(Vector.Up() * self.jump_speed), impulse=True)
            self.jump_timer = 0
            # rb.velocity = Vector.Up() * self.jump_speed #), impulse=True)

    def on_update(self, ev: events.Update, _):
        try:
            inputs = ServiceProvider.getInputs()
        except:
            pass
        else:
            # Jump
            if inputs.get_key_down(Keys.Space) and self.canJump:
                # and self.on_ground
                self.jump_timer = time.monotonic() + self.jump_delay

            # Move Left or Right
            self.direction = Vector.Zero()
            if inputs.get_key_down(self.LEFT_KEY):
                self.direction = Vector.Left() * abs(self.move_flexibility)
            if inputs.get_key_down(self.RIGHT_KEY):
                self.direction = Vector.Right() * abs(self.move_flexibility)

            if inputs.get_key_down(self.UP_KEY):
                self.direction = Vector.Up() * abs(self.move_flexibility)
            if inputs.get_key_down(self.DOWN_KEY):
                self.direction = Vector.Down() * abs(self.move_flexibility)

            if self.direction.x and self.direction.y:
                direction = self.direction.normalize()
            else:
                direction = self.direction

            # rigid body
            rb = self.entity.getComponent(RigidBody)
            if rb is None:
                self.entity.position += Vector(direction * self.speed * ev.delta_time)

    def MovePlayer(self, direction: Vector):
        rb = self.entity.getComponent(RigidBody)
        if rb is not None:
            # if rb.type == RigidBodyType.KINEMATIC:
            # print(self.B_LT, self.B_RT, self.B_UP, self.B_DN, self.entity.position)
            if self.B_DN < self.entity.position.y + direction.y < self.B_UP and self.B_LT < self.entity.position.x + direction.x < self.B_RT:
                rb.move_position(self.entity.position + direction)
            else:
                if not self.B_DN < self.entity.position.y + direction.y:
                    rb.move_position(Vector(self.entity.position.x, self.B_DN + .1))
                elif not self.entity.position.y + direction.y < self.B_UP:
                    rb.move_position(Vector(self.entity.position.x, self.B_UP - .1))

                if not self.B_LT < self.entity.position.x + direction.x:
                    rb.move_position(Vector(self.entity.position.x, self.B_LT + .1))
                elif not self.entity.position.x + direction.x < self.B_RT:
                    rb.move_position(Vector(self.entity.position.x, self.B_LT - .1))

    def on_init(self, ev, _):
        self.animator = self.entity.getComponent(Animator)

    def flip(self):
        self.facingRight = not self.facingRight
        if self.facingRight:
            self.entity.scale.x = abs(self.entity.scale.x)
        else:
            self.entity.scale.x = -abs(self.entity.scale.x)

    def on_fixed_update(self, ev: events.FixedUpdate, _):
        if self.jump_timer > time.monotonic() and self.on_ground:
            self.Jump()

        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction

        rb = self.entity.getComponent(RigidBody)
        if rb is not None:
            if rb.body is not None:
                if rb.body_type == RigidBodyType.KINEMATIC:
                    self.MovePlayer(direction * self.speed * ev.fixed_delta_time)
                elif rb.body_type == RigidBodyType.DYNAMIC:
                    if direction != Vector.Zero():
                        rb.add_force(Vector.Right() * math.copysign(1, direction.x) * self.speed)

                        if abs(rb.velocity.x) > self.max_speed:
                            rb.velocity = Vector(math.copysign(self.max_speed, rb.velocity.x), rb.velocity.y)

                    changing_direction = (
                            (direction.x > 0 and rb.velocity.x < 0)
                            or (direction.x < 0 and rb.velocity.x > 0)
                    )
                    if (direction.x > 0 and not self.facingRight) or (direction.x < 0 and self.facingRight):
                        self.flip()

                    if self.animator is not None:
                        self.animator["velx"] = abs(rb.velocity.x)
                        self.animator["vely"] = rb.velocity.y

                    if self.on_ground:
                        if (abs(direction.x) < 0.4 or changing_direction):
                            rb.drag = self.drag
                        else:
                            rb.drag = 0
                    else:
                        rb.drag = 0
                        rb.gravity_scale = 1
                        rb.drag = self.drag * .15
                        if rb.velocity.y < 0:
                            rb.gravity_scale = self.fall_multiplier
                        elif rb.velocity.y > 0 and not Inputs.get_key_down(Keys.Space):
                            rb.gravity_scale = self.fall_multiplier / 2
