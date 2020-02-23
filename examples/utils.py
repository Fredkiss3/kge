""" This file tests the circle method of utilities module. """

# Dependencies
import pyglet

""" Pyglet utilities. Designed to ease drawing of primitives with Pyglet. """

# Dependencies
import pyglet
from math import sin, cos, radians

def circle(x, y, r, p, c, b): # p is number of points in circle EXCLUDING center
    """ Adds a vertex list of circle polygon to batch and returns it. """
    deg = 360 / p
    deg = radians(deg)
    P = x, y # P for POINTS
    for i in range(p):
        n = deg * i
        P += int(r * cos(n)) + x, int(r * sin(n)) + y
    return b.add(p+1, pyglet.gl.GL_TRIANGLE_FAN, None, ('v2i', P), ('c3B', (c)))

# Constants
WIN = 800, 800, 'TEST', False, 'tool' # x, y, caption, resizable, style
CENTER = WIN[0] // 2, WIN[1] // 2
RADIUS = 300
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
SPEED = 0.005 # in seconds

# Variables
win = pyglet.window.Window(*WIN)
batch = pyglet.graphics.Batch()
points = 1 # excluding center

def on_step(dt):
    """ Logic performed every frame. """
    global batch, points
    batch = pyglet.graphics.Batch()
    points += 1 # 2, 3, 4...
    print (points + 1) # total number of points
    circle(CENTER[0], CENTER[1], RADIUS, points, WHITE+MAGENTA*(points), batch)

@win.event
def on_draw():
    """ Drawing perfomed every frame. """
    win.clear()
    batch.draw()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(on_step, SPEED)
    pyglet.app.run()