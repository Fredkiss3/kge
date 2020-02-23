# import time
#
# import pyglet
#
# class HelloWorldWindow(pyglet.window.Window):
#     """
#     Hello World Window
#     """
#     # def __init__(self, **kwargs):
#     #     super(HelloWorldWindow, self).__init__(**kwargs)
#
#     dt = time.monotonic()
#     fps = 0
#
#
#
#
# # SET RESSOURCES PATH
# # pyglet.resource.path = ['../resources']
# # pyglet.resource.reindex()
#
# # CENTER IMAGE
# def center_image(image):
#     """Sets an image's anchor point to its center"""
#     image.anchor_x = image.width // 2
#     image.anchor_y = image.height // 2
#
# if __name__ == '__main__':
#     # window = HelloWorldWindow()
#     # window.set_caption("COUCOU")
#     pyglet.app.run()

# !/usr/bin/python
# $Id:$

# import random
# import sys
#
# from pyglet.gl import *
# from pyglet import font
# from pyglet import graphics
# from pyglet import window
#
#
# MAX_PARTICLES = 2000
# if len(sys.argv) > 1:
#     MAX_PARTICLES = int(sys.argv[1])
# MAX_ADD_PARTICLES = 100
# GRAVITY = -100
#
#
# def add_particles():
#     particle = batch.add(1, GL_POINTS, None,
#                          ('v2f/stream', [win.width / 2, 0]))
#     particle.dx = (random.random() - .5) * win.width / 4
#     particle.dy = win.height * (.5 + random.random() * .2)
#     particle.dead = False
#     particles.append(particle)
#
#
# def update_particles(dt):
#     global particles
#     for particle in particles:
#         particle.dy += GRAVITY * dt
#         vertices = particle.vertices
#         vertices[0] += particle.dx * dt
#         vertices[1] += particle.dy * dt
#         if vertices[1] <= 0:
#             particle.delete()
#             particle.dead = True
#     particles = [p for p in particles if not p.dead]
#
#
# def loop(dt):
#     update_particles(dt)
#     for i in range(min(MAX_ADD_PARTICLES, MAX_PARTICLES - len(particles))):
#         add_particles()
#
# win = window.Window(vsync=False)
# batch = graphics.Batch()
# particles = list()
#
#
# @win.event
# def on_draw():
#     win.clear()
#     batch.draw()
#
# clock = pyglet.app.event_loop.clock
# if __name__ == '__main__':
#
#     clock.schedule(loop)
#     pyglet.app.run()


from pyglet.gl import *
from pyglet.window import Window
from pyglet import app
from pyglet.clock import Clock

from threading import Thread, Lock, Event

gl_lock = Lock()


class ManagedWindow(Window):
    """
    A pyglet window with an event loop which executes automatically
    in a separate thread. Behavior is added by creating a subclass
    which overrides setup, update, and/or draw.
    """
    fps_limit = 30
    default_win_args = dict(width=600,
                            height=500,
                            vsync=False,
                            resizable=True)

    def __init__(self, **win_args):
        """
        It is best not to override this function in the child
        class, unless you need to take additional arguments.
        Do any OpenGL initialization calls in setup().
        """
        self.win_args = dict(self.default_win_args, **win_args)
        self.Thread = Thread(target=self.__event_loop__)
        self.Thread.start()


    def __event_loop__(self, **win_args):
        """
        The event loop thread function. Do not override or call
        directly (it is called by __init__).
        """
        gl_lock.acquire()
        try:
            try:
                super(ManagedWindow, self).__init__(**self.win_args)
                self.switch_to()
                self.setup()
                app.run()
            except Exception as e:
                print("Window initialization failed: %s" % (str(e)))
        finally:
            gl_lock.release()

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_scroll(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_resize(self, w, h):
        pass

    def on_close(self):
        """
        Closes the window.
        """
        self.close()

    def setup(self):
        """
        Called once before the event loop begins.
        Override this method in a child class. This
        is the best place to put things like OpenGL
        initialization calls.
        """
        pass

    def on_update(self, dt):
        """
        Called before draw during each iteration of
        the event loop. dt is the elapsed time in
        seconds since the last update. OpenGL rendering
        calls are best put in draw() rather than here.
        """
        pass

    def on_draw(self):
        """
        Called after update during each iteration of
        the event loop. Put OpenGL rendering calls
        here.
        """
        pass


if __name__ == '__main__':
    ManagedWindow()
