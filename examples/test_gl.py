# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *

# w, h = 500, 500


# def square():
#     glBegin(GL_QUADS)
#     glVertex2f(100, 100)
#     glVertex2f(200, 100)
#     glVertex2f(200, 200)
#     glVertex2f(100, 200)
#     glEnd()


# def iterate():
#     glViewport(0, 0, 500, 500)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()


# def showScreen():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     iterate()
#     glColor3f(1.0, 0.0, 3.0)
#     square()
#     glutSwapBuffers()


# # print(bool(glutInit))
# # exit()
# glutInit()
# glutInitDisplayMode(GLUT_RGBA)
# glutInitWindowSize(500, 500)
# glutInitWindowPosition(0, 0)
# wind = glutCreateWindow("OpenGL Coding Practice")
# glutDisplayFunc(showScreen)
# glutIdleFunc(showScreen)
# glutMainLoop()
import glfw
from OpenGL import GL as gl
import sys
import contextlib
import pyglet
pyglet.sprite.Sprite


@contextlib.contextmanager
def create_main_window():
    if not glfw.init():
        sys.exit(1)
    try:
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        title = 'Tutorial 2: First Triangle'
        window = glfw.create_window(500, 400, title, None, None)
        if not window:
            sys.exit(2)
        glfw.make_context_current(window)

        glfw.set_input_mode(window, glfw.STICKY_KEYS, True)
        gl.glClearColor(0.4, 0.4, 0.4, 0)

        yield window

    finally:
        glfw.terminate()


if __name__ == '__main__':
    with create_main_window() as window:
        while (
            glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
            not glfw.window_should_close(window)
        ):
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            glfw.swap_buffers(window)
            glfw.poll_events()
