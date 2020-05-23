import random
import time
from typing import Dict, List, Type

import kge
from kge import *
from kge import events
from move_mixin import MoveMixin


class FollowPlayer(Behaviour):
    """
    For following the player
    """

    def on_fixed_update(self, ev: events.FixedUpdate, _):
        players = list(ev.scene.get(kind=Player))

        if len(players) > 0:
            player = players[0]
            dest = Vector(player.position.x, self.entity.position.y)

            rb = self.entity.getComponent(RigidBody)
            if rb is not None:
                distance = dest - self.entity.position
                # if distance > Vector.Unit() * 2:
                #     pass
                if distance > Vector.Unit() * 2:
                    dt = ev.fixed_delta_time if isinstance(ev, events.FixedUpdate) else ev.delta_time
                    self.entity.position = Vector.move_towards(self.entity.position, dest,
                                                               10 * dt
                                                               )
                else:
                    # rb.velocity = Vector.Zero()
                    # rb.velocity = Vector(player.rb.velocity.x, rb.velocity.y)
                    # rb.move_position(dest)
                    self.entity.position = dest
            else:
                # to = Vector.move_towards(self.entity.position, dest, 5 * ev.delta_time)
                to = dest
                self.entity.position = to


class Follower(Sprite):
    def on_fixed_update(self, ev: events.FixedUpdate, _):
        players = list(ev.scene.get(kind=Player))

        if len(players) > 0:
            player = players[0]
            dest = Vector(player.position.x, self.position.y)

            # to = Vector.move_towards(self.entity.position, dest, 5 * ev.delta_time)
            to = dest
            self.position = to


class Bg(Sprite):
    def __init__(self):
        # super().__init__(name="Background")
        self.name = "Background"
        self.image = Image("assets/bg_effect.png")
        self.transform.scale = Vector(1000 / 640, 700 / 480)
        self.addComponent(FollowPlayer(self))


class DestructionLayer(Sprite):
    def __init__(self):
        self.scale = Vector(100, 1)
        self.addComponent(BoxCollider(sensor=True))

    def on_collision_enter(self, ev: events.CollisionEnter, _):
        e = ev.collider.entity
        if isinstance(e, Player):
            # ev.collider.entity.destroy()
            check = list(ev.scene.get(tag="checkpoint"))

            if check:
                e.position = check[0].position
                e.getComponent(RigidBody).velocity = Vector.Zero()
                # e.destroy()
                # ev.scene.add(Player(), check[0].position, "Player")
        else:
            print(f"Destroying {ev.collider.entity}")
            ev.collider.entity.destroy()


class Ground(Sprite):
    def __init__(self):
        # super().__init__(tag="ground")
        self.tag = "ground"
        # self.image = OutLinedSquare()

        self.image = Image("assets/ground.png")

        self.addComponent(BoxCollider(
            friction=.01
        ))

    # def on_update(self, ev, _):
    #     print(f"Ground Box : {self.position}")


class GroundRight(Sprite):
    def __init__(self):
        super().__init__()
        self.image = Image("assets/ground_right.png")

    def on_init(self, ev, _):
        self.addComponent(BoxCollider(friction=.1))


class GroundLeft(Sprite):
    def __init__(self):
        super().__init__()
        # self.image = OutLinedSquare(RED)
        self.image = Image("assets/ground_left.png")

    def on_init(self, ev, _):
        self.addComponent(BoxCollider(friction=.1))


class ChildBox(Entity):
    def __init__(self, parent: 'Box'):
        self.parent = parent

    def on_init(self, ev, _):
        self.addComponent(BoxCollider(
            box=Vector.Unit() * .9,
            sensor=True,
        ))

    def on_collision_enter(self, ev, _):
        if ev.collider.entity != self.parent:
            self.parent.opacity = .5

    def on_collision_exit(self, ev, _):
        if ev.collider.entity != self.parent:
            self.parent.opacity = 1


class Box(Sprite):
    def __init__(self):
        self.name = "Box"
        self.image = Image("assets/box.png")
        self.color = WHITE

        # self.image = OutLinedSquare(GREY)
        self.rb = RigidBody(body_type=RigidBodyType.DYNAMIC)
        self.rb.angular_velocity = .5
        self.rb.fixed_rotation = False
        self.addComponent(self.rb)
        self.addComponent(BoxCollider(friction=10,
                                      density=10,
                                      # bounciness=.6
                                      ))
        # self.addComponent(BoxCollider(
        #     box=Vector.Unit() * .75,
        #     sensor=True,
        # ))


class PlayerController(MoveMixin):
    UP_KEY = Keys.Z
    DOWN_KEY = Keys.S
    LEFT_KEY = Keys.Q
    RIGHT_KEY = Keys.D
    speed = 7
    move_flexibility = Vector(1, 0)
    fall_multiplier = 4
    canJump = True
    jump_speed = 8
    max_speed = 7
    drag = 10


# Player animations
root = "platformer/Assets"
player = "Virtual Guy"
idle_sheet = Image(f"{root}/Main Characters/{player}/Idle (32x32).png")
appearing_sheet = Image(f"{root}/Main Characters/Appearing (96x96).png")
run_sheet = Image(f"{root}/Main Characters/{player}/Run (32x32).png")
jump = Image(f"{root}/Main Characters/{player}/Jump (32x32).png")
fall = Image(f"{root}/Main Characters/{player}/Fall (32x32).png")
wall_sheet = Image(f"{root}/Main Characters/{player}/Wall Jump (32x32).png")
idle = idle_sheet.slice(Vector(32, 32))
run = run_sheet.slice(Vector(32, 32))
appear = appearing_sheet.slice(Vector(96, 96))
wall = wall_sheet.slice(Vector(32, 32))

# Double the animation length
len_ = len(appear)
for i in range(0, len_ * 2, 2):
    appear.insert(i + 1, appear[i])

# Bg Image
bg_im = TiledImage(f"{root}/Background/Purple.png", Vector(24, 12))

#
size = 16
terrain = Image(f"{root}/Terrain/Terrain Sliced (16x16).png")
terrains = terrain.slice(Vector.Unit() * size)
# print(len(terrains))
brick = terrains[133]


# Fruits
class Fruit(Sprite):
    root = f"{root}/Items/Fruits"

    def __init__(self, name="Apple"):
        sheet = Image(f"{self.root}/{name}.png").slice(Vector.Unit() * 32)
        self.image = sheet[0]

        self.scale *= 2
        self.name = f"{name} {self.nbItems}"

        # Set animations
        idle = Animation.from_sequence(self, sheet, .05, name="idle")
        collected = Animation.from_spritesheet(self, Image(f"{self.root}/Collected.png"), Vector.Unit() * 32, .05,
                                               name="collected", loop=False)

        # print(collected.length)
        self.animator = Animator(idle, collected)

        # Add Field and transitions
        self.animator.add_field("is_collected", False)
        self.animator.add_transition(
            idle, collected, C(is_collected=True)
        )

        # Add components
        self.addComponents(
            self.animator,
            # RigidBody(),
            CircleCollider(
                sensor=True,
                bounciness=1,
                radius=1 / 4
            )
        )

    def on_collision_enter(self, ev: events.CollisionEnter, _):
        if isinstance(ev.collider.entity, Player) and not isinstance(ev.collider, BoxCollider):
            self.animator["is_collected"] = True

            self.getComponent(Collider).is_active = False
            self.start_coroutine(lambda: self.destroy(), .4)
            print(f"Player collected {self.name}")


class Player(Sprite):
    def __init__(self):
        self.name = "player"
        self.tag = "player"
        self.image = idle[0]
        # self.image = Square()
        # self.visible = False
        self.scale *= 2

        idle_anim = Animation.from_sequence(self, idle, .05, 'idle')
        run.insert(0, run[-1])
        run_anim = Animation.from_sequence(self, run, .05, 'run', )
        wall_anim = Animation.from_sequence(self, wall, .05, 'wall jump', loop=True)

        jump_anim = Animation(
            self, [Frame(image=jump, duration=1)], loop=False, name='jump'
        )

        fall_anim = Animation(
            self, [Frame(image=fall, duration=1)], loop=False, name='fall'
        )

        appear_anim = Animation.from_sequence(self, [
            *appear, appear[-1]
        ], .05, 'appear', loop=False)

        # SETTING UP AN ANIMATOR
        # Animator
        self.animator = Animator(
            appear_anim,
            wall_anim,
            idle_anim,
            run_anim,
            jump_anim,
            fall_anim,
        )

        # Fields
        self.animator.add_field('on_ground', True)
        self.animator.add_field('velx', 0)
        self.animator.add_field('vely', 0)
        self.animator.add_field('wall', False)

        # Conditions
        grounding = C(on_ground=True)
        running = C(velx__gt=0.4)
        jumping = C(vely__gt=0.5)
        falling = C(vely__lt=-0.4)
        touching_wall = C(wall=True)

        # Transitions
        self.animator.add_transition(appear_anim, fall_anim, ALWAYS)
        self.animator.add_transition(ANY, fall_anim, falling & ~grounding)
        self.animator.add_transition(ANY, jump_anim, jumping)
        self.animator.add_transition(ANY, wall_anim, touching_wall)
        #self.animator.add_transition(wall_anim, fall_anim, ~touching_wall & falling)
        #self.animator.add_transition(wall_anim, jump_anim, ~touching_wall & jumping)
        self.animator.add_transition(wall_anim, idle_anim, ~touching_wall & grounding)
        self.animator.add_transition(jump_anim, fall_anim, falling)
        self.animator.add_transition(fall_anim, idle_anim, grounding & ~running)
        self.animator.add_transition(fall_anim, run_anim, grounding & running)
        self.animator.add_transition(idle_anim, run_anim, running & grounding, ~running & grounding)
        for (s, c), t in self.animator.transitions.items():
            print(t, "==>", c)

        self.rb = RigidBody()
        self.rb.gravity_scale = 1
        self.rb.fixed_rotation = True
        self.rb.gravity_scale = 1
        self.controller = PlayerController()

        # Add animator
        self.addComponent(self.animator)
        self.addComponent(self.controller)
        self.addComponent(self.rb)
        self.addComponent(BoxCollider(
            box=Vector(.56, .56),
            offset=Vector(0, .01),
            density=1.5,
            friction=0
        ))

        self.addComponent(
            CircleCollider(
                density=.5,
                center=Vector(0, -.2),
                radius=.3,
                friction=0
            )
        )

        self.ray_dist = .6
        self.overlap_size = Vector.Unit() * 5
        self.colliders = []
        self.offsetx = .2
        self.offsety = .1
        self.wall = False
        self.ray_wall_l = .35


    def on_update(self, ev, _):
        # print(self.components)
        try:
            self.colliders = []
            hit = Physics.ray_cast(Vector(self.position.x - self.offsetx, self.position.y), Vector.Down(),
                                   self.ray_dist, )
            hit2 = Physics.ray_cast(Vector(self.position.x + self.offsetx, self.position.y), Vector.Down(),
                                    self.ray_dist, )
            hit3 = Physics.ray_cast(self.position, Vector.Down(),
                                    self.ray_dist, )
            hit4 = Physics.ray_cast(self.position, Vector.Right(),
                                    self.ray_wall_l, )
            hit5 = Physics.ray_cast(self.position, Vector.Left(),
                                    self.ray_wall_l, )
            # hits = physics.query_region(self.position, self.overlap_size, layer="Foreground")
            # self.colliders = hits.colliders

            self.colliders = [hit.collider, hit2.collider, hit3.collider, hit4.collider, hit5.collider, ]

            grounded = hit.collider is not None or hit2.collider is not None or hit3.collider is not None
            wall = (hit4.collider is not None and Inputs.get_key_down(Keys.D)) or (hit5.collider is not None and Inputs.get_key_down(Keys.Q))  
            self.animator["on_ground"] = grounded
            self.animator["wall"] = wall
            #print(wall)

            if grounded != self.controller.on_ground:
                self.controller.on_ground = grounded
        except:
            pass

    # def on_anim_changed(self, ev: events.AnimChanged, _):
    #     print(ev.previous, ev.next)
    #     print(self.animator["on_ground"])

    def on_draw_debug(self, ev, _):
        debug = DebugDraw

        o = Vector(self.position.x - self.offsetx, self.position.y)
        o2 = Vector(self.position.x + self.offsetx, self.position.y)
        debug.draw_segment(o, o + Vector.Down() * self.ray_dist, BLUE)
        debug.draw_segment(o2, o2 + Vector.Down() * self.ray_dist, BLUE)
        debug.draw_segment(self.position, self.position + Vector.Down() * self.ray_dist, BLUE)
        debug.draw_segment(self.position, self.position + Vector.Left() * self.ray_wall_l, BLUE)
        debug.draw_segment(self.position, self.position + Vector.Right() * self.ray_wall_l, BLUE)
        # debug.draw_box(self.position, self.overlap_size, BLUE, solid=True)

        for col in self.colliders:
            if isinstance(col, BoxCollider):
                debug.draw_box(col.offset * col.entity.transform, col.box * 2, RED, solid=False)
            if isinstance(col, CircleCollider):
                debug.draw_circle(col.offset * col.entity.transform, col.radius, RED, solid=False)


class Ball(Sprite):
    def __init__(self):
        self.name = "Ball"
        self.image = Image("assets/ball.png")
        self.scale = Vector.Unit()
        self.addComponents(RigidBody())
        self.addComponents(CircleCollider(
            bounciness=.08, center=Vector(-.03, 0), radius=1 / 6))

        self.selected = False
        self.mouse_pos = Vector.Zero()

    def on_mouse_motion(self, ev: events.MouseMotion, _):
        self.mouse_pos = ev.position + ev.delta

    def on_mouse_drag(self, ev: events.MouseDrag, _):
        self.mouse_pos = ev.position + ev.delta

    def on_update(self, ev, _):
        if Inputs.get_mouse_down(Mouse.Primary):
            # print(e_b)
            e_b = kge.Box(self.position, self.scale)
            m_b = kge.Box(self.mouse_pos, Vector.Unit() / 2)
            if e_b.overlaps(m_b):
                self.getComponent(RigidBody).move_position(Vector(self.mouse_pos))
                self.selected = True
        else:
            self.selected = False

    def on_draw_debug(self, ev, _):
        color = BLUE
        if self.selected:
            color = RED
        DebugDraw.draw_box(self.position, self.scale, color)
        DebugDraw.draw_box(self.mouse_pos, Vector.Unit() / 2, BLUE)


class CameraFollow(Behaviour):
    def __init__(self):
        super().__init__()
        self.follow_object = None
        self.threshold = None
        self.follow_offset = Vector(9, 6)
        self.speed = 10
        self.move_speed = Vector.Zero()
        # self.next_position =

    def on_init(self, ev: events.Init, _):
        self.follow_object = list(ev.scene.get(kind=Player))[0]
        self.threshold = self.calculate_treshold()
        self.speed = 3
        self.next_pos = Vector.Zero()

    # def on_late_update(self, ev: events.LateUpdate, _):
    #     rb = self.entity.getComponent(RigidBody)
    #     # rb.move_position(self.next_pos)
    #     # self.entity.position = Vector.move_towards(self.entity.position,
    #     #                                            Vector(self.next_pos.x, -self.next_pos.y),
    #     #                                            self.move_speed * ev.delta_time)
    #
    #     vel =  self.follow_object.getComponent(RigidBody).velocity
    #     rb.velocity = Vector(vel.x, rb.velocity.y)

    def on_fixed_update(self, ev: events.FixedUpdate, _):
        self.threshold = self.calculate_treshold()

        follow = self.follow_object.position

        x_diff = (Vector.Right() * self.entity.position.x).distance_to(Vector.Right() * follow.x)
        y_diff = (Vector.Up() * self.entity.position.y).distance_to(Vector.Up() * follow.y)

        rb = self.entity.getComponent(RigidBody)
        # rb.velocity = Vector.Zero()
        follow_rb = self.follow_object.getComponent(RigidBody)

        self.next_pos = Vector(self.entity.position)

        if abs(x_diff) >= self.threshold.x:
            print("Passing out of treshold !")
            self.next_pos = Vector(follow.x, self.entity.position.y)

        # rb.velocity = Vector(follow_rb.velocity.x, rb.velocity.y)
        # if abs(y_diff) >= self.threshold.y:
        #     pos.y = follow.y

        # print(self.threshold)

        if follow_rb.velocity.magnitude > self.speed:
            self.move_speed = follow_rb.velocity.magnitude
        else:
            self.move_speed = self.speed

        # self.entity.position = Vector.move_towards(self.entity.position, Vector(pos.x, -pos.y),
        #                                            speed * ev.fixed_delta_time)
        # rb.velocity = Vector(speed)

        # print(rb.velocity)

        rb = self.entity.getComponent(RigidBody)
        # rb.move_position(self.next_pos)
        # self.entity.position = Vector.move_towards(self.entity.position,
        #                                            Vector(self.next_pos.x, -self.next_pos.y),
        #                                            self.move_speed * ev.delta_time)

        vel = self.follow_object.getComponent(RigidBody).velocity
        rb.velocity = Vector(vel.x, rb.velocity.y)

    def on_draw_debug(self, ev, _):
        border = self.calculate_treshold()
        DebugDraw.draw_box(self.entity.position, border * 2, RED)
        DebugDraw.draw_box(Vector(*self.entity.transform.xf.position), Vector.Unit() / 10, BLUE, solid=True)

    def calculate_treshold(self):
        t = Vector(self.entity.scene.Right - self.entity.scene.Left, self.entity.scene.Top - self.entity.scene.Bottom)

        t.x -= self.follow_offset.x
        t.y -= self.follow_offset.y

        return t


class Brick(Sprite):
    def __init__(self):
        self.image = brick
        self.scale *= 4
        self.addComponent(BoxCollider(
            box=Vector.Unit()
        ))


class Tilemap(Entity):
    def __init__(self, pattern: List, entities: Dict[int, Type[Entity]], cell_size: int = 1):
        self.pattern = pattern
        self.entities = entities
        self.cell_size = cell_size

    def cell_at(self, x, y):
        n = self.pattern[x][y]
        if n in self.entities:
            return self.entities[n]
        return None

    def on_init(self, ev: events.Init, _):
        off_x = ev.scene.main_camera.half_width
        off_y = ev.scene.main_camera.half_height - self.cell_size / 2

        for j in range(len(self.pattern)):
            if isinstance(self.pattern[j], list):
                for i in range(len(self.pattern[j])):
                    if isinstance(self.pattern[j][i], list):
                        raise TypeError("Only two dimensionnal lists are permitted")
                    e = self.cell_at(j, i)
                    if e is not None:
                        pos = Vector(i - off_x, -j + off_y)
                        e = e()
                        ev.scene.add(e, pos, layer=5)
                        print(
                            f"Adding {e} at {pos} | {ev.scene.main_camera.half_width, ev.scene.main_camera.half_height}")
            else:
                raise TypeError("Only two dimensionnal lists are permitted")


def setup(scene: Scene):
    DebugDraw.setFlags(
        # drawColliders=True,
        # drawEntities=True,
        drawStuff=True,
    )
    scene.background_color = BLACK
    # Set layer
    scene.setLayer(0, "Background")
    scene.setLayer(1, "Ground")
    scene.setLayer(2, "Foreground")
    scene.setLayer(3, "Player")
    scene.setLayer(4, "Box")
    Physics.ignore_layer_collision("Player", "Box")
    # s = Sprite(image=brick)
    # s.scale *= 4
    # scene.add(s, layer=5)
    pattern = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

    ]
    # scene.add(Tilemap(pattern=pattern, entities={1: Brick}))

    # Add component to main camera
    # scene.display_fps = True
    scene.main_camera.addComponent(
        # CameraFollow())
        FollowPlayer())
    # CameraController())

    # Add entities
    p = Player()
    # # scene.main_camera.parent = p
    scene.add(p, position=Vector(0, -4), layer="Player")
    # # scene.add(Sprite(name='player', tag='player'), position=Vector(-1, 0), layer="Player")
    scene.add(Entity(name="checkpoint", tag="checkpoint"), position=Vector(0, -4), layer="Player")
    # scene.add(Player(), position=Vector(-2, -4), layer="Player")
    fruits = [
        "Apple", "Bananas", "Cherries", "Kiwi", "Melon", "Orange", "Pineapple", "Strawberry"
    ]
    # #
    # b = Box()
    # scene.add(b, position=Vector(0, 0), layer="Box")
    # scene.add(ChildBox(b), position=Vector(0, 0), layer="Foreground")
    x = 0
    for j in range(-3, -2):
        for i in range(-21, 20, 3):
            if i != 0:
                random.seed(time.time())
                x += 1
                scene.add(Fruit(random.choice(fruits)), position=Vector(i, j), layer='Player')

    print(x, "Fruits !!")
    scene.add(DestructionLayer(), position=Vector(0, -6), layer="Foreground")

    # bg = Sprite(Image("assets/bg_effect.png"), name="Bg")
    # bg.scale = Vector(1000 / 640, 700 / 480)
    # # bg.addComponent(FollowPlayer())
    # bg.parent = scene.main_camera

    # scene.add(bg, position=Vector.Zero(), layer="Background")

    # for j in range(5, -6, -1):
    #     for i in range(-8, 10, 1):
    bg = Sprite(image=bg_im, name="Bg")
    # bg.parent = scene.main_camera
    scene.add(bg)

    x = 0
    for i in range(-25, 24):
        for j in range(-5, -6, -1):
            x += 1
            gd = Sprite(name=f"ground {x}", tag="ground", image=brick)
            gd.scale *= 4
            gd.addComponent(BoxCollider(
                friction=.01,
                box=Vector.Unit()
            ))
            if i == -25 or i == 23:
                scene.add(gd, position=Vector(i, j + 1), layer="Ground")
            else:
                scene.add(gd, position=Vector(i, j), layer="Ground")

    # scene.add(Ball(), position=Vector(-1, 0), layer="Ground")

    # follower = Sprite(name="Follower")
    # follower = Follower()
    # # follower2 = Follower()
    # follower3 = Follower()
    # follower4 = Follower()
    # follower4.opacity = follower3.opacity = 1
    # # follower.visible = False

    # follower.addComponent(RigidBody(RigidBodyType.DYNAMIC))
    # follower.position = Vector(0, -4)
    # follower2.addComponent(RigidBody(RigidBodyType.KINEMATIC))
    # follower3.addComponent(RigidBody(RigidBodyType.KINEMATIC))
    # follower4.addComponent(RigidBody(RigidBodyType.KINEMATIC))
    # follower.addComponent(FollowPlayer())

    # follower.parent = scene.main_camera
    # follower2.parent = scene.main_camera
    # follower3.parent = scene.main_camera
    # follower4.parent = scene.main_camera
    # scene.add(follower, position=Vector(-1, -1), layer="Player")
    # scene.add(follower2, position=Vector(-1, 1), layer="Player")
    # scene.add(follower3, position=Vector(1, -1), layer="Player")
    # scene.add(follower4, position=Vector(1, 1), layer="Player")
    print("Dirties :", len(scene.dirties))


if __name__ == '__main__':
    import logging
    kge.run(
            setup,
            pixel_ratio=32,
            resolution=Vector(1366, 720),
            #show_output=True,
            show_fps=True,
            # resizable=False,
            vsync=False,
            #log_level=logging.DEBUG
            )
