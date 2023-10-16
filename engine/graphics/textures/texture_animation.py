from enum import Enum

import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture import Texture
from engine.util.util import get_texture


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


class TextureAnimation:

    def __init__(self, surface: pygame.Surface, animation_type: AnimationType, sprite_width: int, time: float = 0.2,
                 loop: bool = True, scale: Vector = Vector(1, 1)):
        self.surface = surface
        self.animation_type = animation_type
        self.sprite_width = sprite_width
        self.sprite_height = self.surface.get_height()

        self.timer = 0
        self.count = 0
        self.target_time = time
        self.loop = loop

        self.textures = self._load_textures()
        self.scale = self.set_scale(scale)

    def _load_textures(self):
        textures = []
        for x in range(self.surface.get_width() // self.sprite_width):
            textures.append(get_texture(self.surface, self.sprite_width, self.sprite_height, x * self.sprite_width, 0))
        return textures

    def get_texture(self) -> Texture:
        return self.textures[self.count]

    def update(self, delta_time: float):
        self.timer += delta_time
        if self.timer >= self.target_time:
            self.count += 1
            self.timer -= self.target_time
            if self.count >= len(self.textures):
                if self.loop:
                    self.count = 0
                else:
                    self.count -= 1

    def set_scale(self, scale: Vector):
        for texture in self.textures:
            texture.set_scale(scale)
        return scale

    def reset(self):
        self.timer = 0
        self.count = 0

    def mirror(self, x_axis: bool = False, y_axis: bool = False):
        for texture in self.textures:
            texture.mirror(x_axis, y_axis)

    def copy(self):
        return TextureAnimation(self.surface, self.animation_type, self.sprite_width, self.target_time, self.loop,
                                self.scale)
