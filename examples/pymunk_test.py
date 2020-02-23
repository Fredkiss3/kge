from pymunk.pyglet_util import DrawOptions
import pymunk as pm

import pyglet as pgl


# window
win = pgl.window.Window(1000, 700, vsync=True)

# options for rendering
options = DrawOptions()

# space
space = pm.Space()
space.gravity = (0, -10)

# add a body
body = pm.Body(1, 1)
body.position = 500, 700
body.angular_velocity = 12
body.velocity = (0, -20)


# add a box shape
poly = pm.Poly.create_box(body, (50, 50))

# body.shapes.add(poly)

# add a body to the space, should add with all shape in one call
space.add(body, poly)


@win.event
def on_draw():
    win.clear()
    space.debug_draw(options)


def update(dt):
    space.step(dt)
    print(body.position)


if __name__ == '__main__':
    pgl.clock.schedule_interval(update, 1 / 60)
    pgl.app.run()
