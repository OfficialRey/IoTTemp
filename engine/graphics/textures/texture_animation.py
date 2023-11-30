from enum import Enum
from typing import Tuple

import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture import Texture


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

    def __init__(self, surface: pygame.Surface = None, sprite_width: int = 1,
                 animation_type: AnimationType = None, time: float = 0.2, loop: bool = True,
                 scale: Vector = Vector(1, 1), information: Tuple = None):
        if information is not None:
            # Format: surface, sprite_width, animation_type, target_time, loop, textures, flash_textures, scale
            self.surface = information[0].copy()
            self.sprite_width = information[1]
            self.animation_type = information[2]
            self.target_time = information[3]
            self.loop = information[4]
            self.textures = [texture.copy() for texture in information[5]]
            self.flash_textures = [texture.copy() for texture in information[6]]
            self.scale = information[7]
            self.sprite_height = self.surface.get_height()
        else:
            self.surface = surface
            self.sprite_width = sprite_width
            self.animation_type = animation_type
            self.target_time = time
            self.loop = loop
            self.sprite_height = self.surface.get_height()

            self.textures, self.flash_textures = self._load_textures()
            self.scale = self.set_scale(scale)
            self._update_flash_textures()

        self.timer = 0
        self.count = 0

    def _load_textures(self):
        textures, flash_textures = [], []
        for x in range(self.surface.get_width() // self.sprite_width):
            texture = Texture(
                self.surface.subsurface((x * self.sprite_width, 0, self.sprite_width, self.sprite_height)))
            if not texture.is_empty():
                textures.append(texture)
                flash_textures.append(texture.copy())
        return textures, flash_textures

    def _update_flash_textures(self):
        for flash_texture in self.flash_textures:
            flash_texture.colorize(0)

    def get_texture(self) -> Texture:
        return self.textures[self.count]

    def get_flash_texture(self):
        return self.flash_textures[self.count]

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
        for flash_texture in self.flash_textures:
            flash_texture.set_scale(scale)

        self._update_flash_textures()
        return scale

    def offset_animation(self, value: float):
        self.count = int(value / self.target_time)
        self.timer = value % self.target_time

    def reset(self):
        self.timer = 0
        self.count = 0

    def mirror(self, x_axis: bool = False, y_axis: bool = False):
        for texture in self.textures:
            texture.mirror(x_axis, y_axis)
        for flash_texture in self.flash_textures:
            flash_texture.mirror(x_axis, y_axis)

    def copy(self):
        # Format: surface, sprite_width, animation_type, target_time, loop, textures, flash_textures, scale
        return TextureAnimation(information=(
            self.surface, self.sprite_width, self.animation_type, self.target_time, self.loop, self.textures,
            self.flash_textures, self.scale))
