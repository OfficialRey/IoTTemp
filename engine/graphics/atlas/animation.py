import os
from typing import List

import pygame

from engine.core.vector import Vector
from engine.graphics.animation.animation import AnimationType, AnimationData
from engine.graphics.textures.texture import Texture
from engine.util.debug import print_debug
from engine.util.resources import get_resource_path


class AnimationAtlas:

    def __init__(self, path: str, file_name: str, animation_types: List[AnimationType],
                 sprite_width: int, sprite_height: int, animation_time: float = 0.2, loop: bool = True,
                 rotation_precision: int = 360):

        print_debug(f"Creating animation atlas {path}/{file_name}")

        self.surface = pygame.image.load(
            os.path.join(get_resource_path(), os.path.join(path, file_name))).convert_alpha()

        self.animation_types = animation_types
        self.animation_time = animation_time
        self.loop = loop
        self.rotation_precision = rotation_precision

        self.base_width = sprite_width
        self.base_height = sprite_height

        self.x_length = self.surface.get_width() // self.base_width
        self.y_length = self.surface.get_height() // self.base_height
        self.count = self.x_length * self.y_length

        self.textures: List[Texture] = []
        self.animation_data: List[AnimationData] = []

        self._initialise()

    def _initialise(self):
        self._load_textures()
        self._clean_animation_types()

    def _load_textures(self):
        self.textures = []

        for i in range(len(self.animation_types)):
            animation_type = self.animation_types[i]
            if animation_type is not None:
                surface = self.surface.subsurface(
                    (0, i * self.base_height, self.surface.get_width(), self.base_height))
                textures = self._split_row(surface)
                animation_data = AnimationData(animation_type, len(self.textures), len(self.textures) + len(textures),
                                               self.animation_time, self.loop)

                self.textures.extend(textures)
                self.animation_data.append(animation_data)

    def _split_row(self, surface: pygame.Surface) -> List[Texture]:
        textures = []
        for x in range(surface.get_width() // self.base_width):
            texture = Texture(
                surface.subsurface((x * self.base_width, 0, self.base_width, self.base_height)),
                rotation_precision=self.rotation_precision)
            if not texture.is_empty():
                textures.append(texture)
        return textures

    def _clean_animation_types(self):
        clean_animation_types = []
        for animation_type in self.animation_types:
            if animation_type is not None:
                clean_animation_types.append(animation_type)
        self.animation_types = clean_animation_types

    def get_animation_data(self, animation_type: AnimationType):
        for animation_data in self.animation_data:
            if animation_data.animation_type == animation_type:
                return animation_data
        return None

    def set_scale(self, scale: Vector):
        for texture in self.textures:
            texture.set_scale(scale)

    def set_size(self, width: int, height: int):
        x_scale = width / self.base_width
        y_scale = height / self.base_height
        self.set_scale(Vector(x_scale, y_scale))

    def get_size(self):
        return self.base_width, self.base_height
