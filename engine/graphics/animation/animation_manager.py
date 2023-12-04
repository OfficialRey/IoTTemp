from random import random

import pygame

from engine.graphics.animation.animation import AnimationType, AnimationData
from engine.graphics.atlas.animation import AnimationAtlas
from engine.graphics.textures.texture import Texture


class AnimationManager:

    def __init__(self, animation_atlas: AnimationAtlas, animation_type: AnimationType = AnimationType.GENERIC,
                 flash_speed: float = 0.05):
        self.animation_atlas = animation_atlas
        self.animation_data = None

        self.flash_time = 0
        self.flash_speed = flash_speed
        self.timer = 0
        self.count = 0
        self.rotation = 0
        self._initialise(animation_type)

    def _initialise(self, animation_type: AnimationType):
        self.update_animation_type(animation_type)
        if self.animation_data is None:
            self.update_animation_index(0)

    def update_animation_data(self, animation_data: AnimationData):
        if animation_data is not None:
            self.animation_data = animation_data

    def update_animation_type(self, animation_type: AnimationType):
        self.update_animation_data(self.animation_atlas.get_animation_data(animation_type))

    def update_animation_index(self, index: int):
        self.update_animation_type(self.animation_atlas.animation_types[index])

    def set_rotation(self, rotation: float):
        self.rotation = rotation

    def get_rotation(self):
        return self.rotation

    def flash_image(self, flash_time: float):
        self.flash_time = flash_time

    def update(self, delta_time: float):
        self.timer += delta_time
        if self.timer >= self.animation_data.animation_time:
            self.count += 1
            self.timer -= self.animation_data.animation_time
            if self.count >= self.animation_data.length:
                if self.animation_data.loop:
                    self.count = 0
                else:
                    self.count -= 1

    def offset_animation(self, value: float = 0):
        if value == 0:
            value = random() * self.animation_data.animation_time * self.animation_data.length
        self.count = int(value % self.animation_data.length)
        self.timer = value % self.animation_data.animation_time

    def get_texture(self, animation_atlas: AnimationAtlas) -> Texture:
        return animation_atlas.textures[self.animation_data.start_index + self.count]

    def get_surface(self, animation_atlas: AnimationAtlas) -> pygame.Surface:
        texture = self.get_texture(animation_atlas)
        if self.flash_time > 0 and self.flash_time % self.flash_speed * 2 < self.flash_speed:
            return texture.get_flash_image(self.rotation)
        return texture.get_image(self.rotation)
