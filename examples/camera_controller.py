import time

from kge import *


class CameraController(Behaviour):
    def on_fixed_update(self, ev: events.FixedUpdate, _):
        camera = ev.scene.main_camera
        # print(f"Camera Pos (Update: {time.monotonic()})", camera.position)
        inputs = ServiceProvider.getInputs()

        # movement
        direction = Vector.Zero()
        if inputs.get_key_down(Keys.Right):
            direction += Vector.Right()
        if inputs.get_key_down(Keys.Left):
            direction += Vector.Left()
        if inputs.get_key_down(Keys.Up):
            direction += Vector.Down()
        if inputs.get_key_down(Keys.Down):
            direction += Vector.Up()

        # zoom
        camera.position += direction * 10 * ev.fixed_delta_time

    def on_key_up(self, ev: events.KeyUp, _):
        camera = ev.scene.main_camera
        if ev.key is Keys.NumpadPlus:
            camera.zoom *= 2
        elif ev.key is Keys.NumpadMinus:
            camera.zoom /= 2
        if ev.key is Keys.C:
            camera.zoom = 1
            camera.position = Vector.Zero()
