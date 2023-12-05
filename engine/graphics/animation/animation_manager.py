from random import random

import pygame

from engine.graphics.animation.animation import AnimationType, AnimationData
from engine.graphics.atlas.animation import AnimationAtlas
from engine.graphics.atlas.atlas import Atlas
from engine.graphics.textures.texture import Texture


class AnimationManager:

    def __init__(self, atlas: Atlas, animation_type: AnimationType = AnimationType.GENERIC,
                 flash_speed: float = 0.05):
        self.atlas = atlas
        self.animation_data = None

        self.previous_animation = None
        self.loop = self.atlas.loop
        self.flash_time = 0
        self.flash_speed = flash_speed
        self.timer = 0
        self.count = 0
        self.rotation = 0

        self.single_play = False

        self._initialise(animation_type)

    def _initialise(self, animation_type: AnimationType):
        self.update_animation_type(animation_type)
        if self.animation_data is None:
            self.update_animation_index(0)

    # Play an animation once
    def single_play_animation(self, animation_type: AnimationType):
        self.single_play = True
        if self.get_animation_data(animation_type) is not self.animation_data:
            self.previous_animation = self.animation_data
            self.update_animation_type(animation_type)
            self.timer = 0
            self.count = 0

    def update_animation_data(self, animation_data: AnimationData):
        if animation_data is not None:
            self.previous_animation = self.animation_data
            self.animation_data = animation_data

    def update_animation_type(self, animation_type: AnimationType):
        if isinstance(self.atlas, AnimationAtlas):
            self.update_animation_data(self.get_animation_data(animation_type))

    def get_animation_data(self, animation_type: AnimationType):
        return self.atlas.get_animation_data(animation_type)

    def update_animation_index(self, index: int):
        self.update_animation_data(self.atlas.animation_data[index])

    def loop_animation(self, loop: bool):
        self.loop = loop

    def set_rotation(self, rotation: float):
        self.rotation = rotation

    def get_rotation(self):
        return self.rotation

    def flash_image(self, flash_time: float):
        self.flash_time = flash_time

    def update(self, delta_time: float):
        self.flash_time -= delta_time
        self.timer += delta_time
        if self.timer >= self.animation_data.animation_time:
            self.count += 1
            self.timer -= self.animation_data.animation_time
            if self.count >= self.animation_data.length:
                self.on_repeat_animation()
                if self.animation_data.loop:
                    self.count = 0
                else:
                    self.count -= 1

    def offset_animation(self, value: float = 0):
        if value == 0:
            value = random() * self.animation_data.animation_time * self.animation_data.length
        self.count = int(value % self.animation_data.length)
        self.timer = value % self.animation_data.animation_time

    def get_texture(self, atlas: Atlas) -> Texture:
        return atlas.textures[self.animation_data.start_index + self.count]

    def get_surface(self, atlas: Atlas) -> pygame.Surface:
        texture = self.get_texture(atlas)
        if self.flash_time > 0 and self.flash_time % self.flash_speed * 2 < self.flash_speed:
            return texture.get_flash_image(self.rotation)
        return texture.get_image(self.rotation)

    def is_animation_finished(self):
        if not self.loop:
            return self.count == self.animation_data.length - 1

    def on_repeat_animation(self):
        if self.single_play:
            self.single_play = False
            self.update_animation_data(self.previous_animation)
