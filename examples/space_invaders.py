import logging
import random
import time
from typing import Union

import kge
from kge import *


class Cadre(Entity):
    """
    This object is invisible but helps for deleting bullets which are out of the view
    """

    def __init__(self, factor: float = 22):
        super().__init__()
        self.image = OutLinedSquare(RED)
        scale_factor = factor

        # Collider and scale
        self.scale = Vector.Unit() * scale_factor
        self.addComponent(EdgeCollider(
            vertices=[
                v * scale_factor for v in Vector.Box()
            ],
            isSensor=True
        ))

    def on_collision_enter(self, ev: physics_events.CollisionEnter, _):
        # Destroy the bullet
        if isinstance(ev.collider.entity, Bullet):
            ev.collider.entity.destroy()


class Bullet(Sprite):
    """
    The Bullet
    """

    def __init__(self, direction: Vector):
        super().__init__()
        gr = [*YELLOW]
        gr[3] = 125
        self.transform.scale = Vector.Unit() / 8
        self.image = Circle(gr, self.scale.x)

        # The speed of the bullet
        self.speed = 3

        # Set velocity and add collider
        self.rb = RigidBody()
        self.rb.gravity_scale = 0
        self.rb.velocity = direction.normalized() * self.speed
        self.addComponent(self.rb)
        self.addComponent(CircleCollider(isSensor=True))


class Aim(Sprite):
    """
    The mouse cursor
    """

    def __init__(self):
        super().__init__()
        self.image = OutlinedCircle(BLUE, 1 / 8)

    def on_mouse_drag(self, ev: events.MouseDrag, _):
        self.position = ev.position

    def on_mouse_motion(self, ev: events.MouseMotion, _):
        self.position = ev.position


class Player(Sprite):
    """
    The player
    """

    def __init__(self):
        super().__init__(None, "player")
        # image and scale
        self.image = Image("assets/player.png")
        self.scale = Vector.Unit() / 1.5

        # For firing bullets
        self.last_fire = None
        self.fire_rate = 10
        self.can_shoot = True

        # Physics Components
        self.rb = RigidBody()  # this helps for applying movement to the game object 
        self.rb.gravity_scale = 0  # We don't want our game object to be fall on gravity
        self.addComponent(self.rb)  # Add rigid body
        self.addComponent(CircleCollider(isSensor=True))  # This helps for responding to collisions

        # bullet sound & score
        self.sound = Sound("assets/laser1.ogg")
        self.score = 0

    def on_init(self, ev, _):
        debug = ServiceProvider.getDebug()
        debug.flags = {
            # "drawShapes": True
        }

    def on_mouse_motion(self, ev: events.MouseMotion, _):
        self.rb.angle = Vector.Up().angle_to(ev.position)

    def on_mouse_drag(self, ev: events.MouseDrag, _):
        """
        Change the rotation of the body if mouse is moving
        """
        # print(self.rb.body is not None)
        self.rb.angle = ev.position.angle

    def on_update(self, ev: events.Update, _):
        # Adjusting fire rate (10 bullets / sec), modify fire_rate in order to change the number
        # of bullets per second
        if self.last_fire is None:
            self.last_fire = time.time()

        if time.time() - self.last_fire >= 1 / self.fire_rate:
            self.can_shoot = True
        else:
            self.can_shoot = False

        # If can shoot then 
        if self.can_shoot:
            # get Inputs
            inputs = ServiceProvider.getInputs()

            # If left mouse button has been clicked
            if inputs.get_mouse_down(Mouse.Primary):
                # position of the click
                pos = Vector(self.position + Vector.Up() / 2).rotated(self.angle)
                # Shoot if mouse left clicked and can_shoot
                ev.scene.add(Bullet(Vector.Up().rotated(self.angle)), position=pos)

                # last time fired is now
                self.last_fire = time.time()

                # Play Fire sound
                # self.sound.play()


class GameOver(Text):
    """
    Game Over Text
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = "GAME OVER"
        self.color = BLUE
        self.font_size = 30
        self.bold = True


class RestartText(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = "APPUYEZ SUR R POUR REDEMARRER"
        self.color = BLUE
        self.font_size = 30
        self.bold = True

    def on_key_down(self, event: events.KeyDown, _):
        if event.key is Keys.R:
            Scene.load(setup_or_scene=setup)


class Score(Text):
    """
    Text to display the score of the player
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = BLUE
        self.font_size = 24
        self.bold = True

    def on_update(self, ev: events.Update, _):
        # Get the player and display its score (if the player is in scene)
        targets = list(ev.scene.get(kind=Player))
        if targets:
            player = targets[0]
            self.value = f'Score : {player.score}'


class Enemy(Sprite):
    """
    An enemy
    """

    def __init__(self, speed=1.5):
        super().__init__()
        # image and scale
        self.image = Triangle(RED)
        self.transform.scale = Vector.Unit() / 1.5

        # Physics Components
        self.rb = RigidBody()
        self.rb.gravity_scale = 0
        self.addComponent(self.rb)
        self.addComponent(TriangleCollider(isSensor=True))

        # the target of the enemy
        self.target = None  # type: Union[Player, None]
        # the speed of the enemy
        self.speed = speed
        self.death_sound = Sound("assets/bomb.wav")
        self.game_over = Sound("assets/death.wav")

    def on_collision_enter(self, ev: physics_events.CollisionEnter, _):
        # get the enemy spawner
        spawner = list(ev.scene.get(kind=EnemySpawner))
        if spawner: spawner = spawner[0]

        # If collided with player, destroy him
        if isinstance(ev.collider.entity, Player):
            ev.collider.entity.destroy()

            # Stop spawner for adding new enemies
            spawner.stop = True
            self.game_over.play()

            # Show Game Over Text
            ev.scene.add(GameOver(), position=Vector(-2, 0))
            ev.scene.add(RestartText(), position=Vector(-6, -1))

        # If hit by the bullet, destroy self
        elif isinstance(ev.collider.entity, Bullet):
            self.destroy()
            ev.collider.entity.destroy()
            self.death_sound.play(volume=2)

            # Update the score of the player
            targets = list(ev.scene.get(kind=Player))
            if targets:
                player = targets[0]
                player.score += 1

    def on_update(self, ev: events.Update, _):
        # Get and Set target (player)
        if self.target is None:
            targets = list(ev.scene.get(kind=Player))
            if targets:
                self.target = targets[0]
            else:
                self.target = None

    def on_fixed_update(self, ev: events.FixedUpdate, _):
        if self.target is not None:
            # Move towards target
            dest = Vector.move_towards(self.position, self.target.position, self.speed * ev.fixed_delta_time)
            self.rb.move_position(dest)

            # Rotate towards target
            self.rb.angle = Vector.Up().angle_to(self.position) + 180


class EnemySpawner(Empty):
    """
    The game object responsible for adding enemies at a certain time in the scene
    """

    def __init__(self):
        super().__init__()
        # For invoking enemies
        self.last_wave = None  # Last wave of enemies
        self.wave_time_span = 2  # Time between wave of enemies
        self.last_spawn = None  # Last time an enemy has been spawned
        self.distance = 9  # Distance to spawn enemies
        self.stop = False  # Variable for stopping enemy spawning
        self.enemies_speed = 1.5  # The base speed of enemies
        self.enemies_time_span = 1  # The Time between each spawn of enemy

        # Background Music
        self.music = Sound("assets/bg_music.mp3")
        self.music.play(volume=0, loop=True)

    def on_update(self, ev: events.Update, _):
        if not self.stop:
            if self.last_wave is None:
                self.last_wave = time.time()
                self.change_wave()

            # Change Enemy speed if it is time to a new wave
            if time.time() - self.last_wave >= self.wave_time_span:
                self.last_wave = time.time()
                self.change_wave()

            if self.last_spawn is None:
                self.last_spawn = time.time()


            # Each second spawn a new enemy
            elif time.time() - self.last_spawn >= self.enemies_time_span:
                self.last_spawn = time.time()
                scene = ev.scene

                # Place an enemy at random position
                side = random.choice([
                    Vector(self.distance, random.randint(-self.distance, self.distance)),
                    Vector(-self.distance, random.randint(-self.distance, self.distance)),
                    Vector(random.randint(-self.distance, self.distance), self.distance),
                    Vector(random.randint(-self.distance, self.distance), -self.distance),
                ])
                scene.add(Enemy(self.enemies_speed), position=side)

    def change_wave(self):
        """
        Change a wave
        each time enemies become more faster
        """
        # Change enemies speed
        self.enemies_speed += 1 / 4


class MenuText(Text):
    def __init__(self):
        super(MenuText, self).__init__()
        self.value = "Appuyez sur Espace pour commencer la partie"
        self.color = BLUE
        self.font_size = 24

    def on_key_up(self, ev: events.KeyDown, _):
        if ev.key is Keys.Space:
            Scene.load(setup)


def menu(scene: "kge.Scene"):
    scene.background_color = WHITE

    scene.add(MenuText(), position=Vector(-5, 0))


def setup(scene: "kge.Scene"):
    """
    Setup function used to start a scene
    """

    # Uncomment this to display the FPS
    # scene.display_fps = True

    # Uncomment this line if you want to control the camera
    #   Use UP, DOWN, LEFT, RIGHT, arrow keys to move around
    #   And +, - to zoom in and zoom out
    # scene.main_camera.addComponent(CameraController())

    # Bg color
    scene.background_color = WHITE
    # scene.display_fps = True

    # Add all objects
    scene.add(Player(), Vector(0, 0))
    scene.add(Aim())
    scene.add(Cadre())
    scene.add(EnemySpawner())
    scene.add(Score(), position=Vector(-4, -5))


if __name__ == '__main__':
    kge.run(menu,
            # Set to debug if you want to see colliders and rigidBodies
            # log_level=logging.DEBUG,
            log_level=logging.INFO,
            )
