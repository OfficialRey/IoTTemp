import os
from typing import List

import pygame.image

from engine.core.vector import Vector
from engine.graphics.atlas.atlas import Atlas
from engine.graphics.textures.texture import Texture
from engine.util.debug import print_debug
from engine.util.resources import get_resource_path

PATH = "path"
FILE = "file"
SPRITE_WIDTH = "sprite_width"
SPRITE_HEIGHT = "sprite_height"
SCALED_WIDTH = "scaled_width"
SCALED_HEIGHT = "scaled_height"


class LevelAtlas(Atlas):

    def __init__(self, path: str, file_name: str, sprite_width: int, sprite_height: int, scaled_width: int = None,
                 scaled_height: int = None):
        super().__init__(path, file_name, sprite_width, sprite_height)

        print_debug(f"Creating level atlas {path}/{file_name}")

        self.textures = self._load_textures()

        if scaled_width is not None and scaled_height is not None:
            x_scale = scaled_width // self.sprite_width
            y_scale = scaled_height // self.sprite_height
            self.scale_textures(Vector(x_scale, y_scale))

    def _load_textures(self) -> List[Texture]:
        textures = self._load_spawn_points()
        for y in range(self.y_length):
            for x in range(self.x_length):
                texture = Texture(self.surface.subsurface(
                    (x * self.sprite_width, y * self.sprite_height, self.sprite_width, self.sprite_height)))
                if not texture.is_empty():
                    textures.append(texture)
        return textures

    def _load_spawn_points(self):
        path = os.path.join(get_resource_path(), self.path)
        textures = [
            Texture(pygame.image.load(os.path.join(path, "player_spawn.png"))),
            Texture(pygame.image.load(os.path.join(path, "enemy_spawn.png")))
        ]
        return textures

    def __getitem__(self, item: int) -> Texture:
        return self.textures[item]

    def get_dict(self) -> dict:
        return {
            PATH: self.path,
            FILE: self.file_name,
            SPRITE_WIDTH: self.sprite_width,
            SPRITE_HEIGHT: self.sprite_height,
            SCALED_WIDTH: self.scaled_width,
            SCALED_HEIGHT: self.scaled_height
        }


def load_atlas(atlas_data: dict) -> LevelAtlas:
    return LevelAtlas(
        atlas_data[PATH],
        atlas_data[FILE],
        atlas_data[SPRITE_WIDTH],
        atlas_data[SPRITE_HEIGHT],
        atlas_data[SCALED_WIDTH],
        atlas_data[SCALED_HEIGHT]
    )
