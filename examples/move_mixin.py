import math

from kge import *


class MoveMixin(Component):
    """
    Move component
    """
    direction = Vector(0, 0)
    speed = 20
    max_speed = 7
    jump_speed = 3
    canJump = False
    move_flexibility = Vector.Up()
    LEFT_KEY = Keys.Left
    RIGHT_KEY = Keys.Right
    DOWN_KEY = Keys.Down
    UP_KEY = Keys.Up

    def __init__(self, BoundUp: float=float("inf"), BoundBottom: float=-float("inf"), BoundLeft: float=-float("inf"), BoundRight: float=float("inf")):
        super().__init__()
        self.B_UP = BoundUp
        self.B_DN = BoundBottom
        self.B_LT = BoundLeft
        self.B_RT = BoundRight
        self.on_ground = False

    def Jump(self):
        rb = self.entity.getComponent(RigidBody)
        if rb is not None:
            rb.velocity = Vector(rb.velocity.x, 0)
            rb.add_force(Vector(Vector.Up() * self.jump_speed), True)

    def on_update(self, ev: events.Update, _):
        inputs = ServiceProvider.getInputs()

        # Jump
        if inputs.get_key_down(Keys.Space) and self.on_ground and self.canJump:
            self.Jump()

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

    def on_fixed_update(self, ev: events.FixedUpdate, _):
        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction

        rb = self.entity.getComponent(RigidBody)
        if rb is not None:
            if rb.body is not None:
                self.MovePlayer(direction * self.speed * ev.fixed_delta_time)
