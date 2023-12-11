import os
from typing import List

import pygame.image

from engine.graphics.atlas.atlas import Atlas
from engine.graphics.textures.texture import Texture
from engine.util.debug import print_debug


class LevelAtlas(Atlas):

    def __init__(self, path: str, file_name: str, sprite_width: int, sprite_height: int):
        super().__init__(path, file_name, sprite_width, sprite_height)

        print_debug(f"Creating level atlas {path}/{file_name}")

        self.textures = self._load_textures()

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
        textures = [
            Texture(pygame.image.load(os.path.join(self.path, "player_spawn.png"))),
            Texture(pygame.image.load(os.path.join(self.path, "enemy_spawn.png")))
        ]
        return textures

    def __getitem__(self, item: int) -> Texture:
        return self.textures[item]
