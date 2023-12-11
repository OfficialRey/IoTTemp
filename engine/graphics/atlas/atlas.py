import os
from abc import ABC
from typing import List, Tuple

import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture import Texture
from engine.util.resources import get_resource_path


class Atlas(ABC):

    def __init__(self, path: str, file_name: str, sprite_width: int, sprite_height: int, rotation_precision: int = 360):
        self.path = os.path.join(get_resource_path(), path)
        self.file_name = file_name
        self.surface = pygame.image.load(os.path.join(self.path, self.file_name)).convert_alpha()
        self.sprite_scale = Vector(1, 1)
        self.sprite_width, self.sprite_height = sprite_width, sprite_height
        self.scaled_width, self.scaled_height = sprite_width, sprite_height
        self.rotation_precision = rotation_precision

        self.x_length = self.surface.get_width() // self.sprite_width
        self.y_length = self.surface.get_height() // self.sprite_height
        self.count = self.x_length * self.y_length
        self.textures: List[Texture] = []

    def scale_textures(self, scale: Vector):
        for texture in self.textures:
            texture.scale_texture(scale)
        self.sprite_scale *= scale
        self.scaled_width *= scale.x
        self.scaled_height *= scale.y

    def get_average_radius(self):
        return self.get_average_texture_size() / 2

    def get_average_texture_size(self):
        return (self.get_texture_width() + self.get_texture_height()) / 2

    def get_texture_width(self):
        return int(self.sprite_width * self.sprite_scale.x)

    def get_texture_height(self):
        return int(self.sprite_height * self.sprite_scale.y)

    def get_texture_size(self) -> Tuple[int, int]:
        return self.get_texture_width(), self.get_texture_height()

    def count_surfaces(self):
        count = 0
        for texture in self.textures:
            count += 1 + len(texture.images) + len(texture.flash_images)

        return count

    def _split_row(self, surface: pygame.Surface) -> List[Texture]:
        textures = []
        for x in range(surface.get_width() // self.sprite_width):
            texture = Texture(
                surface.subsurface((x * self.sprite_width, 0, self.sprite_width, self.sprite_height)),
                rotation_precision=self.rotation_precision)
            if not texture.is_empty():
                textures.append(texture)
        return textures
