import kge
# from camera_controller import CameraController
from kge import *

root = Image("flappy.png")

##################################
######       RESOURCES     #######
##################################

# Bg
bg_sky = root.cropped(Vector(0, 256), Vector(144, 256))
bg_night = root.cropped(Vector(146, 256), Vector(144, 256))

# bird anim
bird = root.cropped(Vector.Zero(), Vector.Unit() * 25)
bird2 = root.cropped(Vector(28, 0), Vector.Unit() * 25)
bird3 = root.cropped(Vector(56, 0), Vector.Unit() * 25)

# others
grass = root.cropped(Vector(293, 512 - 57), Vector(168, 55))
pipe_up = root.cropped(Vector(83, 25), Vector(27, 164))
pipe_down = root.cropped(Vector(56, 25), Vector(27, 164))
play_btn = root.cropped(Vector(352, 512 - 150), Vector(54, 34))
title_img = root.cropped(Vector(350, 512 - 116), Vector(90, 28))

# Animations
step = .1
flappy_frames = [
    Frame(image=bird, duration=step),
    Frame(image=bird2, duration=step),
    Frame(image=bird3, duration=step),
]

step = .1
title_frames = [
    Frame(position=Vector.Up() * 4, duration=step),
    Frame(position=Vector.Up() * 3.97, duration=step),
    Frame(position=Vector.Up() * 3.94, duration=step),
    Frame(position=Vector.Up() * 3.91, duration=step),
    Frame(position=Vector.Up() * 3.9, duration=step),
    Frame(position=Vector.Up() * 3.91, duration=step),
    Frame(position=Vector.Up() * 3.94, duration=step),
    Frame(position=Vector.Up() * 3.97, duration=step),
    Frame(position=Vector.Up() * 4, duration=step),
]

title_smooth = [
    Frame(position=Vector.Up() * 4, duration=.5),   # 0
    Frame(position=Vector.Up() * 3.8, duration=.5), # 1
    Frame(position=Vector.Up() * 4, ),   # 2
]

cam_frames = [
    Frame(position=Vector.Zero(), duration=2),
    Frame(position=Vector.Up() * 5, duration=2),
    Frame(position=Vector.Zero()),
]

class CamShaker(Behaviour):
    def on_init(self, ev, _):
        self.shake_anim = Animation(
            self.entity, cam_frames,
            loop=False,
            function=Animation.Smooth,
        )

    def on_update(self, ev, _):
        self.shake_anim.update()

#
# title_op = [
#     Frame(opacity)
# ]


class Bird(Sprite):
    def __init__(self, **_):
        super().__init__(**_)
        self.image = bird
        self.scale *= 3

        self.rb = RigidBody()
        self.addComponent(self.rb)
        self.addComponent(
            BoxCollider(
                Vector(12 / 64, 12 / 64) * 3,
                offset=Vector.Up() * .15
            )
        )
        self.addComponent(
            CircleCollider(
                18 / 64,
                center=Vector(-.15, .15)
            )
        )
        self.addComponent(
            CircleCollider(
                18 / 64,
                center=Vector(.15, .15)
            )
        )
        self.animation = Animation.from_sequence(
            self, [bird, bird2, bird3, bird], step)

        self.addComponent(Animator(
            self.animation
        ))

    # def on_update(self, ev, _):
    #     self.animation.update()

    def on_fixed_update(self, ev, _):
        if Inputs.get_key_down(Keys.Space):
            self.rb.velocity = Vector(0, 5)

        # print(self.position)
    # def on_collision_begin(self, ev, _):
    #     print("Collision Begin", ev.collider)


class Ground(Sprite):
    def __init__(self):
        super().__init__()
        self.image = grass
        self.scale *= 3

        self.addComponent(BoxCollider(
            Vector(168 / 64, 55 / 64) * 3,
        ))


class StaticGround(Sprite):
    def __init__(self):
        super().__init__()
        self.image = grass
        self.scale *= 3


class Pipe(Sprite):
    def __init__(self, up=True):
        super().__init__()
        if up:
            self.image = pipe_up
        else:
            self.image = pipe_down

        self.scale *= 3
        self.addComponent(BoxCollider(
            Vector(27 / 64, 162 / 64) * 3
        ))


class Goal(Empty):
    pass


class StaticBird(Sprite):
    def __init__(self, **_):
        super().__init__(**_)
        self.image = bird
        self.scale *= 3
        self.animation = Animation.from_sequence(
            self, [bird, bird2, bird3, bird], step)

        self.addComponent(Animator(
            self.animation
        ))

    # def on_update(self, ev, _):
    #     self.animation.update()
        # print(self.animation)


class Menu(Canvas):
    def __init__(self, scale: Vector):
        self.scale = scale

        title = Panel(
            title_img
        )

        title.size = Vector(3.5, 1) * 1.5

        play = Button(
            "",
            self.launchGame,
            style=ButtonStyle(
                bg=play_btn
            )
        )

        copy = Text(
            "Made with Kiss Game Engine",
            font=Font(
                color=Color(84, 56, 71),
                name="Kenney Pixel",
                file="Kenney Pixel.ttf",
                bold=True,
                size=20,
            )
        )

        copy.size = Vector(self.scale.x, 1)

        anim = Animation(
            title,
            frames=title_smooth,
            function=Animation.Smooth
        )

        self.addComponent(
            Animator(
                anim
            )
        )

        self.add(title, Vector.Up() * 4)
        self.add(play, Vector.Down())
        self.add(copy, Vector.Down() * 4.8)

    def launchGame(self):
        Scene.load(GameScene)

class GameOver(Canvas):
    def __init__(self, **_):
        super().__init__(**_)


class GameScene(Scene):
    def setup(self):
        self.setLayer(0, "bg")
        self.setLayer(1, "mid")
        self.setLayer(2, "fg")
        self.display_fps = True

        bg = Sprite(image=bg_sky)
        bg.scale *= 3
        self.add(bg, layer="bg")

        bd_up = Entity(name="border up")
        bd_up.scale = Vector(4, 1)
        bd_up.addComponent(BoxCollider())

        self.add(bd_up, Vector(0, self.Top) + Vector.Unit() / 2, layer="fg")
        self.add(Bird(), Vector.Up(), layer="fg")
        self.add(Ground(), position=Vector.Down() * 5, layer="fg")
        # self.add(Menu(scale=Vector(self.Right - self.Left, self.Top - self.Bottom)))


class MenuScene(Scene):
    def setup(self):
        DebugDraw.setFlags(drawEntities=True)

        # self.main_camera.addComponent(CameraController())
        # self.main_camera.addComponent(CamShaker())
        self.setLayer(0, "bg")
        self.setLayer(1, "mid")
        self.setLayer(2, "fg")

        # self.main_camera.addComponent(CameraController())

        bg = Sprite(image=bg_sky)
        bg.scale *= 3
        self.add(bg, layer="bg")
        self.add(StaticBird(), Vector.Up(), layer="fg")
        self.add(StaticGround(), position=Vector.Down() * 5, layer="fg")
        self.add(Menu(scale=Vector(self.Right - self.Left, self.Top - self.Bottom)))
        # self.add(Pipe(), position=Vector.Down() * 3, layer="mid")
        # self.add(Pipe(False), position=Vector.Up() * 3, layer="mid")


if __name__ == '__main__':
    # import logging
    kge.run(
        resolution=Vector(144, 256) * 3,
        starting_scene=MenuScene,
        title="Flappy Bird",
        resizable=True,
        show_console=True,
        # vsync=True,
        # log_level=logging.DEBUG
    )
