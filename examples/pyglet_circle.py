# circle.py
# by Dave Pape, for DMS 423
#
# draws a circle, where the points for the vertex list are computed at run-time
import random

from math import *
from pyglet.gl import *

window = pyglet.window.Window(resizable=True)


def makeCircle(numPoints):
    verts = []
    for i in range(numPoints):
        angle = radians(float(i) / numPoints * 360.0)
        x = 100 * cos(angle) + 300
        y = 100 * sin(angle) + 200
        verts += [x, y]
    global circle
    circle = pyglet.graphics.vertex_list(numPoints, ('v2f', verts))


makeCircle(100)

batch = pyglet.graphics.Batch()
rect = None


@window.event
def on_mouse_press(x, y, buttons, modifiers):
    global rect
    rect = pyglet.graphics.vertex_list(4, ('v2f', [x, y, x - 50, y, x - 50, y - 50, x, y - 50]))

    batch.add(8, GL_LINES, None, ('v2f',
                                      [
                                          # Horizontal
                                          x, y,
                                          x - 50, y,
                                          x - 50, y - 50,
                                          x, y - 50,
                                          # Vertical
                                          x, y - 50,
                                          x, y,
                                          x - 50, y,
                                          x - 50, y - 50,
                                      ]
                                  )
              )


@window.event
def on_resize(w, h):
    print("Resizing !!")



@window.event
def on_draw():
    global circle, rect
    # glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    glColor3f(1, 1, 0)
    window.clear()
    # batch.add(circle)
    circle.draw(GL_TRIANGLE_FAN)

    x, y = random.randint(0, window.width), random.randint(0, window.height)

    batch.add(4, GL_QUADS, None, ('v2f',
                                      [x, y, x - 50, y, x - 50, y - 50, x, y - 50]))
    #
    # if rect is not None:
    #     rect.draw(GL_LINE_LOOP)
    batch.draw()


def rebatch(dt):
    global batch
    # batch = pyglet.graphics.Batch()
    print("Rebatching !")

pyglet.clock.schedule_interval(rebatch, .5)
pyglet.app.run()
#
# while True:
#     pass
