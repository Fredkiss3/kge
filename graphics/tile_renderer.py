from typing import List

import pyglet

import kge
from kge.utils.vector import Vector
from kge.graphics.image import Image
from kge.graphics.sprite_renderer import SpriteRenderer
from kge.resources.events import AssetLoaded


class TileRenderer(SpriteRenderer):

    def __init__(self, entity):
        super().__init__(entity)

        self._tiles = []  # type: List[List[pyglet.sprite.Sprite]]

    def on_asset_loaded(self, ev: AssetLoaded, dispatch):
        """
        If Image has been loaded for this entity then, create the sprite for it
        """
        if isinstance(ev.asset, Image):
            if self._image is not None:
                # Load the asset if it has the same name as self
                if ev.asset.name == self._image.name and self._sprite is None:
                    # print(f'Loading Sprite... for {self.entity}\n')
                    try:
                        # Get batch & group from window service
                        win = kge.ServiceProvider.getWindow()
                        batch = win.batch
                        layers = win.render_layers

                        scale = self.entity.transform.scale

                        for x in range(scale.y):
                            line = []
                            for y in range(scale.x):
                                sprite = pyglet.sprite.Sprite(
                                    img=self._image.load(), subpixel=True,
                                    batch=batch,
                                    group=layers[self.entity.layer]
                                )
                                line.append(sprite)
                            self._tiles.append(line)

                    except Exception as e:
                        import traceback
                        # print(f"Error : {e}")
                        traceback.print_exc()
                    else:
                        # print(f"Asset loaded ==> {ev.asset.name} {self._image.name} Yes !\n")
                        pass

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, val):
        if not isinstance(val, (Image)):
            raise TypeError(
                f"image should be of type 'kge.Image'")
        self._image = val

    def render(self, scene: "kge.Scene", ):
        """
        Render the sprite
        """
        # get camera
        camera = scene.main_camera

        if self.entity is None or not isinstance(self.entity, kge.TileGrid):
            raise AttributeError(
                "Sprite renderer components should be attached to Sprites ('kge.Sprite')")
        else:
            # print(self._tiles)
            if not camera.in_frame(self.entity):
                # If not in camera sight then the sprite should be invisible
                for line in self._tiles:
                    for sprite in line:
                        if sprite.visible:
                            sprite.visible = False
            else:
                for x in range(len(self._tiles)):
                    for y in range(len(self._tiles[x])):
                        sprite = self._tiles[x][y]
                        if not sprite.visible:
                            sprite.visible = True

                        # calculate offset of the sprite
                        offset = Vector(y + 1 / 2, x + 1 / 2)

                        # calculate the offset of the anchor of the sprite
                        anchor = self.entity.position - self.entity.transform.scale / 2

                        # calculate sprite position in world
                        new_pos = anchor + offset

                        # calculate sprite position in screen
                        pos = camera.world_to_screen_point(new_pos)

                        # Then update the sprite
                        sprite.update(pos.x, pos.y,
                                      scale_x=camera.zoom,
                                      scale_y=camera.zoom)
