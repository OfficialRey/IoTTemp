import os.path

from typing import List, Tuple

import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture import Texture
from engine.util.debug import print_debug
from engine.util.resources import get_resource_path


class LevelAtlas:

    def __init__(self, path: str, file_name: str, sprite_width: int, sprite_height: int):
        print_debug(f"Creating level atlas {path}/{file_name}")
        self.image = pygame.image.load(os.path.join(get_resource_path(), os.path.join(path, file_name))).convert_alpha()
        self.path = path
        self.file_name = file_name

        self.base_width = sprite_width
        self.base_height = sprite_height

        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.atlas_width = self.image.get_width()
        self.atlas_height = self.image.get_height()
        self.x_length = self.atlas_width // self.sprite_width
        self.y_length = self.atlas_height // self.sprite_height
        self.count = self.x_length * self.y_length

        self.textures = self._load_sheet()

    def set_scale(self, scale: Vector):
        for texture in self.textures:
            texture.set_scale(scale)
        texture = self.textures[0]
        self.sprite_width, self.sprite_height = texture.get_image().get_size()

    def set_size(self, width: int, height: int):
        x_scale = width / self.base_width
        y_scale = height / self.base_height
        self.set_scale(Vector(x_scale, y_scale))

    def get_texture_size(self) -> Tuple[int, int]:
        return self.sprite_width, self.sprite_height

    def _load_sheet(self) -> List[Texture]:
        textures = []
        for y in range(self.y_length):
            for x in range(self.x_length):
                texture = Texture(self.image.subsurface(
                    (x * self.sprite_width, y * self.sprite_height, self.sprite_width, self.sprite_height)))
                if not texture.is_empty():
                    textures.append(texture)
        return textures

    def __getitem__(self, item: int) -> Texture:
        return self.textures[item]


