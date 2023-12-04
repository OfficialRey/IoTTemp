import os
from enum import Enum
from typing import List

import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture import Texture
from engine.util.debug import print_debug
from engine.util.resources import get_resource_path


class AnimationType(Enum):
    GENERIC = -1
    IDLE = 0
    WALKING_GENERAL = 1

    # Compass
    WALKING_N = 2
    WALKING_S = 3
    WALKING_W = 4
    WALKING_E = 5

    WALKING_NE = 6
    WALKING_SE = 7
    WALKING_SW = 8
    WALKING_NW = 9

    # Actions
    ATTACK = 10
    DAMAGED = 11
    DODGE = 12
    DEATH = 13


class AnimationData:

    def __init__(self, animation_type: AnimationType, start_index: int, end_index: int, animation_time: float,
                 loop: bool):
        self.animation_type = animation_type
        self.start_index = start_index
        self.stop_index = end_index
        self.length = self.stop_index - self.start_index
        self.animation_time = animation_time
        self.loop = loop


class AnimationAtlas:

    def __init__(self, path: str, file_name: str, animation_types: List[AnimationType],
                 sprite_width: int, sprite_height: int, animation_time: float = 0.2, loop: bool = True,
                 rotation_precision: int = 360):

        print_debug(f"Creating animation atlas {path}/{file_name}")

        self.surface = pygame.image.load(
            os.path.join(get_resource_path(), os.path.join(path, file_name))).convert_alpha()

        self.animation_types = animation_types
        self.sprite_width, self.sprite_height = sprite_width, sprite_height
        self.animation_time = animation_time
        self.loop = loop
        self.rotation_precision = rotation_precision

        self.base_width = sprite_width
        self.base_height = sprite_height

        self.textures = []
        self.animation_data = []

        self._initialise()

    def _initialise(self):
        self._load_animations()
        self._clean_animation_types()

    def _load_animations(self):
        self.textures = []

        for i in range(len(self.animation_types)):
            animation_type = self.animation_types[i]
            if animation_type is not None:
                surface = self.surface.subsurface(
                    (0, i * self.sprite_height, self.surface.get_width(), self.sprite_height))
                textures = self._split_row(surface)
                animation_data = AnimationData(animation_type, len(self.textures), len(self.textures) + len(textures),
                                               self.animation_time, self.loop)

                self.textures.append(textures)
                self.animation_data.append(animation_data)

    def _clean_animation_types(self):
        clean_animation_types = []
        for animation_type in self.animation_types:
            if animation_type is not None:
                clean_animation_types.append(animation_type)
        self.animation_types = clean_animation_types

    def _split_row(self, surface: pygame.Surface) -> List[Texture]:
        textures = []
        for x in range(surface.get_width() // self.sprite_width):
            texture = Texture(
                surface.subsurface((x * self.sprite_width, 0, self.sprite_width, self.sprite_height)))
            if not texture.is_empty():
                textures.append(texture)
        return textures

    def set_scale(self, scale: Vector):
        for texture in self.textures:
            texture.set_scale(scale)

    def set_size(self, width: int, height: int):
        x_scale = width / self.base_width
        y_scale = height / self.base_height
        self.set_scale(Vector(x_scale, y_scale))
