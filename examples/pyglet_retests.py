import pyglet as pgl
from pyglet.gl import *


class Renderer:
    def __init__(self):
        self.win = pgl.window.Window(resizable=True, vsync=True)
        self.batch = pgl.graphics.Batch()
        self.e_loop = pgl.app

    def __enter__(self):
        self.win.on_draw = lambda: self.draw()
        self.win.on_mouse_press = lambda x, y, button, mods: self.draw_circle(x, y)

    def run(self):
        pgl.clock.schedule_interval(lambda dt: print("Interval"), 1/10_000)
        self.e_loop.run()

    def draw(self):
        self.win.clear()
        glClearColor(0, 0, 0, 1)
        glColor3f(1, 1, 0)
        lab = pgl.text.Label("HELLO WORLD", batch=self.batch)
        self.batch.draw()
        print(self.batch.group_map)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def draw_circle(self, x, y):
        draw_circle(self.batch, x, y)



def draw_circle(batch, x, y):
    batch.add(4, GL_LINE_LOOP, None, ('v2f',
                                      [x, y, x - 50, y, x - 50, y - 50, x, y - 50]))


if __name__ == '__main__':
    ren = Renderer()
    with ren:
        ren.run()
