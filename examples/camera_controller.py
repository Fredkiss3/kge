from kge import *


class CameraController(Behaviour):
    def on_update(self, ev: events.Update, _):
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
        camera = ev.scene.main_camera
        if inputs.get_key_down(Keys.NumpadPlus):
            camera.zoom += 1 * ev.delta_time
        elif inputs.get_key_down(Keys.NumpadMinus):
            camera.zoom -= 1 * ev.delta_time

        self.entity.position += direction * 10 * ev.delta_time
