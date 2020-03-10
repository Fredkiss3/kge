from pymunk import Vec2d
import random
import time
from io import BytesIO
from typing import Union, List

import math
import pyglet

# Alpha transparents images
# import pytiled_parser
from pyglet.gl import *

# For key Handling
from pyglet.window import key

# For Mouse Events
from pyglet.window import mouse
import pyglet_ffmpeg2

from pyglet import media

# For audio Service
pyglet_ffmpeg2.load_ffmpeg()
# playing music

music = pyglet.resource.media(
    'assets/bg_music.mp3', streaming=False)  # type: media.Source
# help(music)
# player = music.play()
# player.loop = True
# The batch for drawing all things
main_batch = pyglet.graphics.Batch()

# Configs for graphics rendering, anti aliasing, alpha transparency
# config = pyglet.gl.Config(sample_buffers=1, samples=8, alpha_size = 8)


# window
config = pyglet.gl.Config(sample_buffers=1, samples=8,
                          depth_size=1000, double_buffer=True, alpha_size=8)
window = pyglet.window.Window(fullscreen=False, resizable=True,
                              vsync=True,)  # width=1366, height=768)

background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
ui = pyglet.graphics.OrderedGroup(2)

# config = window.config
# config.sample_buffers = 1
# config.alpha_size = 8
# config.samples = 8
#
# window = pyglet.window.Window(resizable=True, config=config)
# print(window.config)

# config = pyglet.gl.Config(sample_buffers=1, samples=4)
# window = pyglet.window.Window(config=config, resizable=True)

# FPS DISPLAY
fps_display = pyglet.text.Label('', x=window.width - 120, y=20,
                                font_size=24, bold=True,
                                color=(127, 127, 127, 255), batch=main_batch, group=ui)
# pyglet.window.FPSDisplay(window=window)
fps_display1 = pyglet.window.FPSDisplay(window=window)

# Image loading
# image = pyglet.resource.image('assets/player_stand.png')
image = pyglet.image.load('assets/box.png')
coin_img = pyglet.image.load("assets/coin.png")

data = None  # type: Union[bytes, None]

with open('assets/playerBlue_walk1.png', 'rb') as f:
    data = f.read()

# Mouse is invisible
# window.set_mouse_visible(False)
# Changing the cursor
cursor = window.get_system_mouse_cursor(window.CURSOR_SIZE_UP)


# window.set_mouse_cursor(cursor)
# window.set_caption()

def center_anchor(img):
    """
    In order to center anchors should be integers
    """
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    print("Mouse Scrolling !!", scroll_x, scroll_y)


# im_data = im1.get_image_data()  # type: pyglet.image.ImageData

# Loading Images
im1 = pyglet.image.load("playerWalk1.png", BytesIO(data), )  # WITH BYTES
im2 = pyglet.image.load('assets/playerBlue_walk2.png')  # WITH STRINGS
im3 = pyglet.image.load('assets/playerBlue_walk3.png')
# im4 = pyglet.image.load('assets/playerBlue_walk4.png')
# im5 = pyglet.image.load('assets/playerBlue_walk5.png')

# Animation & Frames
frames = [im1, im2, im3, ]  # im4, ]#im5]
#
for im_ in frames:
    center_anchor(im_)

# set the animation Frames
frames = [pyglet.image.AnimationFrame(im, duration=1 / 15) for im in frames]

# set animation
ani = pyglet.image.Animation(frames=frames)

# Keeping the resolution
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

# Background Image
bg_im = pyglet.image.load("assets/bg_effect.png")
bg = pyglet.sprite.Sprite(bg_im, subpixel=True, group=background,
                          batch=main_batch
                          )

bg.scale_x, bg.scale_y = window.width / \
    bg_im.width, window.height / bg_im.height,

# players
players = []  # type: List[pyglet.sprite.Sprite]


# Flip Image
def flip(sprite: pyglet.sprite.Sprite):
    # im1 = pyglet.image.load("playerWalk1.png", BytesIO(data), )
    sprite.update(scale_x=-sprite.scale_x)


class Player:
    def __init__(self, sprite: pyglet.sprite.Sprite, pos: tuple):
        self.sprite = sprite
        self.pos = pos
        vel = [random.choice([-1, 0,  1]), random.choice([-1, 0, 1])]
        if vel[0] == vel[1] and vel[0] == 0:
            vel = [random.choice([-1,  1]), random.choice([-1, 1])]

        self.vel = vel


for i in range(500):
    x, y = random.randint(32, window.width), random.randint(32, window.height)
    sprite = pyglet.sprite.Sprite(ani, x, y,
                                  subpixel=True, group=foreground,
                                  batch=main_batch
                                  )
    p = Player(sprite, pos=(x, y))

    # sprite.image.anchor_x, sprite.image.anchor_y = sprite.width / 2, sprite.height / 2
    players.append(p)

# player.image.anchor_x = player.image.width / 2
# player.image.anchor_y = player.image.height / 2

center_anchor(coin_img)

coin = pyglet.sprite.Sprite(coin_img, 0, 0, subpixel=True,
                            group=ui, batch=main_batch)

# Set Window Icon
window.set_icon(coin_img)

# main_batch.a


# Create a label
# label = pyglet.text.Label(
#     text='Hello, world',
#     font_name='Times New Roman',
#     font_size=36,
#
#     # Position => y is up, x is right
#     x=window.width // 2,
#     y=window.height // 2,
#
#     # alignment
#     anchor_x='center',
#     anchor_y='center',
#     batch=main_batch
# )
#
# label.text = ""
# Text Input
# class TextWidget:
#     def __init__(self, text, x, y, width, batch):
#         self.document = pyglet.text.document.UnformattedDocument(text)
#         self.document.set_style(0, len(self.document.text), dict(color=(0, 0, 0, 55)))
#         font = self.document.get_font()
#         height = font.ascent - font.descent
#
#         self.layout = pyglet.text.layout.IncrementalTextLayout(
#             self.document, width, height, multiline=False, batch=batch)
#         self.caret = pyglet.text.caret.Caret(self.layout)
#
#         self.layout.x = x
#         self.layout.y = y
#
#         # Rectangular outline
#         pad = 2
#         # self.rectangle = Rectangle(x - pad, y - pad, x + width + pad, y + height + pad, batch)
#
#     def hit_test(self, x, y):
#         return (0 < x - self.layout.x < self.layout.width and
#                 0 < y - self.layout.y < self.layout.height)
#
#
# t = TextWidget('This is a tset', 200, 100, 200 - 210, main_batch),

# document = pyglet.text.document.FormattedDocument("Text")
# layout = pyglet.text.layout.IncrementalTextLayout(document, 200, 50)
# caret = pyglet.text.caret.Caret(layout)
# window.push_handlers(caret)


RED = (255, 0, 0, 255)
WHITE = (255, 255, 255, 255)


@window.event
def on_mouse_press(x, y, button, modifiers):
    """
    Mouse Event !!
    """
    # print(x, y)
    if button == mouse.LEFT:
        # print('The left mouse button was pressed.')
        draw_circle(Vec2d(x, y), 45, 25, RED, WHITE)


shouldFlip = False


@window.event
def on_key_press(symbol, modifiers):
    """
    A Key pressed Event hapenned !
    """
    global shouldFlip

    # print(f'A key was pressed {symbol} {modifiers}')
    # if symbol == key.A:
    #     print('The "A" key was pressed.')
    if symbol == key.LEFT:
        glTranslatef(50, 0, 1)
    elif symbol == key.RIGHT:
        glTranslatef(-50, 0, -1)
    if symbol == key.UP:
        glTranslatef(0, -50, 0)
    elif symbol == key.DOWN:
        glTranslatef(0, 50, 0)
    #     print('The left arrow key was pressed.')
    # elif symbol == key.ENTER:
    #     print('The enter key was pressed.')
    #

    if symbol == key.SPACE:
        shouldFlip = True
        # print(f"SHOULD FLIP : {shouldFlip}")
    # elif symbol == key.ESCAPE:
    #     window.close()

    # print(modifiers & key.MOD_CTRL, modifiers & key.LCTRL)


# Make eveything the double of thier original resolution
# glScalef(2.0, 2.0, 0.0)
keys = key.KeyStateHandler()

dd = time.monotonic()
fpss = 0


def draw_circle(pos, angle, radius, outline_color, fill_color):
    circle_center = pos

    # http://slabode.exofire.net/circle_draw.shtml
    num_segments = int(20 * math.sqrt(radius))
    theta = 2 * math.pi / num_segments
    c = math.cos(theta)
    s = math.sin(theta)

    x = radius  # we start at angle 0
    y = 0

    ps = []

    for i in range(num_segments):
        ps += [Vec2d(circle_center.x + x, circle_center.y + y)]
        t = x
        x = c * x - s * y
        y = s * t + c * y

    mode = pyglet.gl.GL_TRIANGLE_STRIP
    ps2 = [ps[0]]
    for i in range(1, int(len(ps) + 1 / 2)):
        ps2.append(ps[i])
        ps2.append(ps[-i])
    ps = ps2
    vs = []
    for p in [ps[0]] + ps + [ps[-1]]:
        vs += [p.x, p.y]

    # c = circle_center + Vec2d(radius, 0).rotated(angle)
    # cvs = [circle_center.x, circle_center.y, c.x, c.y]

    # bg = pyglet.graphics.OrderedGroup(0)
    fg = pyglet.graphics.OrderedGroup(1)

    l = len(vs) // 2

    main_batch.add(len(vs) // 2, mode, fg,
                   ('v2f', vs),
                   ('c4B', fill_color * l))

    # main_batch.
    # main_batch.add(2, pyglet.gl.GL_LINES, fg,
    #                ('v2f', cvs),
    #                ('c4B', outline_color * 2))


window.push_handlers(keys)


# @window.event
def on_draw(*args):
    global dd, fpss
    window.clear()
    # # Enable Alpha transparency
    # glEnable(GL_BLEND)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # print(keys[key.SPACE])
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # Draw a primitive
    # pyglet.graphics.draw(
    #     # Vertices
    #     2,
    #     # Mode (Points in this case
    #     pyglet.gl.GL_POINTS,
    #     # v2i for vertex 2D,
    #     ('v2i',
    #      # The data for each point
    #      # Each two point is a vertex -> if 'v2i'
    #      (100, 100, 30, 35)
    #      )
    # )

    # pyglet.graphics.draw_indexed(2, pyglet.gl.GL_POINTS,
    #                              [0, 1],
    #                              ('v2i', (10, 15, 30, 35))
    #                              )

    # pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
    #                              [0, 1, 2, 0, 2, 3],
    #                              ('v2i', (100, 100,
    #                                       150, 100,
    #                                       150, 150,
    #                                       100, 150))
    #                              )

    # label.draw()
    # image.blit(window.width // 2, window.height // 2)
    # player.draw()

    # player.image = im1
    # player.

    if time.monotonic() - dd >= 1:
        fps_display.text = f"{fpss} FPS"
        fpss = 0
        dd = time.monotonic()

    fpss += 1

    main_batch.draw()
    fps_display1.draw()
    # glClear(GL_COLOR_BUFFER_BIT)
    # glLoadIdentity()
    # glBegin(GL_TRIANGLES)
    # glVertex2f(0, 0)
    # glVertex2f(window.width / 2, 0)
    # glVertex2f(window.width / 2 , window.height)
    # glEnd()
    # fps_display.draw()


# on draw event override
window.on_draw = on_draw

# vertices = [
#     0, 0,
#     window.width, 0,
#     window.width, window.height]
# vertices_gl = (GLfloat * len(vertices))(*vertices)
# glEnableClientState(GL_VERTEX_ARRAY)
# glVertexPointer(2, GL_FLOAT, 0, vertices_gl)
#
#
# @window.event
# def on_draw():
#     glClear(GL_COLOR_BUFFER_BIT)
#     glLoadIdentity()
#     glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 2)


dtt = time.monotonic()
counter = 0

# LOG OUT ALL EVENTS HAPPENNING
window.push_handlers(pyglet.window.event.WindowEventLogger())


def on_animation_end():
    print("Animation End")


# tile_map = pytiled_parser.parse_tile_map("assets/map.tmx")
# print(tile_map.layers)
# print(tile_map.background_color)
# print(tile_map.map_size)

# t_set = tile_map.tile_sets[1]
# tile = t_set.tiles[5]
# image_ = tile.image
#
# print(image_.source, tile.image.trans)


def render(players, dt):
    # print(f"DELTA TIME : {dt}")
    global shouldFlip, im1, main_batch
    for p in players:  # type: pyglet.sprite.Sprite
        sign_x, sign_y = random.choice([-1, 1]), random.choice([-1, 1])
        angle = random.randint(0, 360)
        if shouldFlip:
            # print("FLIPPING...")
            # im1.flip_x = not im1.flip_x  #flip(p.image)
            # type: pyglet.image.ImageData
            # p.image = im1
            # To Change Scale
            # p.update(scale_x=-p.scale_x, )

            flip(p)
    shouldFlip = False
    # print(f"RENDER {dt}")
    # p.update(p.x + sign_x * 1000 * dt, p.y + sign_y * 1000 * dt, )


running = True

# @window.event
# def on_close():
#     global running, event_loop
#     event_loop.has_exit = True
#
#     running = False
#     # window.close()
#     print("EXITING ...")
#     return pyglet.event.EVENT_HANDLED


def func(dt): return render(players, dt)


def rebatch(dt):
    """
    IT SHOULD RENEW BATCH IN ORDER TO DELETE THINGS THAT HAVE BEEN DRAWN
    """
    global main_batch, fps_display, bg, players, coin
    main_batch = pyglet.graphics.Batch()
    fps_display.batch = main_batch
    bg.batch = main_batch

    for p in players:
        p.batch = main_batch
    coin.batch = main_batch


# t = threading.Thread(target=update)


class CustomEventLoop(pyglet.app.EventLoop):
    dt = time.monotonic()
    fps = 0

    def idle(self):
        global keys
        rtype = super(CustomEventLoop, self).idle()

        now = time.monotonic()
        if now - self.dt >= 1:
            print(f"IDLE CALLS : {self.fps}")
            self.dt = now
            self.fps = 0
        self.fps += 1

        # print(list(pyglet.app.windows))
        # print(keys[key.SPACE])

        return rtype

    # def on_window_close(self, window):
    #     print(f"EXITING THE EVENT LOOP : {window}")
    #     evLoop.exit()
    #     return pyglet.event.EVENT_HANDLED


# evLoop =\
event_loop = CustomEventLoop()

#
# @event_loop.event
# def on_window_close(window):
#     print(f"EXITING THE EVENT LOOP : {window}")
#     event_loop.exit()
#     return pyglet.event.EVENT_HANDLED

# c1 = pyglet.clock.Clock()
# c2 = pyglet.clock.Clock()


up_dt = 0
vel_init = Vec2d(1, 1)


def update_coin(dt):
    # coin: pyglet.sprite.Sprite
    global up_dt, coin, vel_init, window, rebatch, players
    #
    # # calculate the number of updates to apply
    # times = (dt + up_dt) // (1 / 60)
    #
    # # accumulate the numbers of updates
    # up_dt = (dt + up_dt) % (1 / 60)
    #
    # # update
    # # print(f"UPDATING !!! {dt}")
    # # for i in range(times):
    # #     print("UPDATE")
    # print(f"UPDATED {times} times")
    new_x, new_y = coin.position[0] + vel_init.x * \
        500 * dt, coin.position[1] + vel_init.y * 500 * dt

    if not (0 < new_x < window.width):
        vel_init.x = -vel_init.x

    if not (0 < new_y < window.height):
        vel_init.y = -vel_init.y

    # coin.update(x=new_x, y=new_y,
    #             scale_x=coin.scale_x + 1 * dt,
    #             scale_y=coin.scale_y + 1 * dt)

    # print(coin.width, coin.height)

    for p in players:
        new_x, new_y = p.sprite.position[0] + p.vel[0] * \
            500 * dt, p.sprite.position[1] + p.vel[1] * 500 * dt

        if new_x < 0:
            new_x = window.width
        elif new_x > window.width:
            new_x = 0

        if new_y < 0:
            new_y = window.height
        elif new_y > window.height:
            new_y = 0

        # if not (0 < new_x < window.width):
        #     p.vel[0] = -p.vel[0]

        # if not (0 < new_y < window.height):
        #     p.vel[1] = -p.vel[1]
        p.sprite.update(x=new_x, y=new_y)
    # rebatch(2)


fix_dt = 0


def fixed_update(dt):
    global fix_dt

    # calculate the number of updates to apply
    times = (dt + fix_dt) // (1 / 50)

    # accumulate the numbers of updates
    fix_dt = (dt + fix_dt) % (1 / 50)

    # update
    # print(f"UPDATING !!! {dt}")
    # for i in range(times):
    #     print("UPDATE")
    print(f"FIX UPDATED {times} times")


if __name__ == '__main__':
    # pyglet.clock.schedule_interval(func, 0.48)
    pyglet.clock.schedule_interval(update_coin, 1 / 70)
    # pyglet.clock.schedule_interval(fixed_update, 0.0175)
    # pyglet.clock.schedule_interval(rebatch, 2)
    # c2.schedule_interval(update, 1 / 10_000)
    # t.start()
    pyglet.app.run()

    # event_loop.clock = c1
    # while not event_loop.has_exit:
    #     c1.tick()
    #     c2.tick()
    #
    #     event_loop.idle()
    # event_loop.run()
    # while running:
    #     pyglet.clock.tick()
    #     for window in pyglet.app.windows:
    #         window.switch_to()
    #         window.dispatch_events()
    #         window.dispatch_event('on_draw')
    #         # print("Rendering !")
    #         # if running:
    #         window.flip()
# while True:
#     pyglet.clock.tick()
# for window in pyglet.app.windows:
#     window.switch_to()
#     window.dispatch_events()
#     window.dispatch_event('on_draw')
#     window.flip()
print("Done !")

"""
# Linear Drag Force
var k:Number = 1e-4 * density * ballWidth * ballWidth;

var dragForce:b2Vec2= new b2Vec2(-k*theBall.GetLinearVelocity().Length()*velX, -k*theBall.GetLinearVelocity().Length()*velY);
"""

"""
READ A TMX FILE :

def read_tmx(tmx_file: str) -> pytiled_parser.objects.TileMap:
    # Given a .tmx, this will read in a tiled map, and return
    # a TiledMap object.
    # 
    # Given a tsx_file, the map will use it as the tileset.
    # If tsx_file is not specified, it will use the tileset specified
    # within the tmx_file.
    # 
    # Important: Tiles must be a "collection" of images.
    # 
    # Hitboxes can be drawn around tiles in the tileset editor,
    # but only polygons are supported.
    # (This is a great area for PR's to improve things.)
    # 
    # :param str tmx_file: String with name of our TMX file
    # 
    # :returns: Map
    # :rtype: TiledMap


    # If we should pull from local resources, replace with proper path
    if tmx_file.startswith(":resources:"):
        import os
        path = os.path.dirname(os.path.abspath(__file__))
        tmx_file = f"{path}/resources/{tmx_file[11:]}"

    tile_map = pytiled_parser.parse_tile_map(tmx_file)

    return tile_map

"""
