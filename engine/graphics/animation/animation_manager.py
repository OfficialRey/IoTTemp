from random import random
from typing import Union

import pygame

from engine.graphics.animation.animation import AnimationType, AnimationData
from engine.graphics.atlas.animation import AnimationAtlas
from engine.graphics.atlas.atlas import Atlas
from engine.graphics.textures.texture import Texture


class AnimationManager:

    def __init__(self, atlas: Atlas, animation_type: AnimationType = AnimationType.GENERIC,
                 flash_speed: float = 0.05):
        self.atlas = atlas
        self.animation_data = []

        for animation_data in self.atlas.animation_data:
            self.animation_data.append(animation_data.copy())

        self.current_animation = None
        self.previous_animation = None

        self.flash_time = 0
        self.flash_speed = flash_speed
        self.rotation = 0
        self.single_play = False

        self._initialise(animation_type)

    def _initialise(self, animation_type: AnimationType):
        self.update_animation_type(animation_type)
        if self.current_animation is None:
            self.update_animation_index(0)

    # Play an animation once
    def single_play_animation(self, animation_type: AnimationType):
        self.single_play = True
        if self.get_animation_data(animation_type) is not self.current_animation:
            self.current_animation.timer = 0
            self.current_animation.count = 0
            self.previous_animation = self.current_animation
            self.update_animation_type(animation_type)

    def update_current_animation(self, timer: float = None, loop: bool = False):
        if timer is not None:
            self.current_animation.timer = timer
        if loop is not None:
            self.current_animation.loop = loop

    def update_animation_data(self, animation_data: AnimationData):
        if animation_data is None:
            return
        if animation_data is self.current_animation:
            return

        self.previous_animation = self.current_animation
        self.current_animation = animation_data
        self.current_animation.timer = 0
        self.current_animation.count = 0

    def update_animation_type(self, animation_type: AnimationType):
        if isinstance(self.atlas, AnimationAtlas):
            self.update_animation_data(self.get_animation_data(animation_type))

    def get_animation_data(self, animation_type: AnimationType) -> Union[AnimationData, None]:
        for animation_data in self.animation_data:
            if animation_data.animation_type == animation_type:
                return animation_data
        return None

    def update_animation_index(self, index: int):
        self.update_animation_data(self.animation_data[index])

    def loop_animation(self, loop: bool):
        self.animation_data.loop = loop

    def set_rotation(self, rotation: float):
        self.rotation = rotation

    def get_rotation(self):
        return self.rotation

    def flash_image(self, flash_time: float):
        self.flash_time = flash_time

    def update(self, delta_time: float):
        self.flash_time -= delta_time
        self.current_animation.timer += delta_time

        if self.current_animation.timer < self.current_animation.animation_time:
            return

        self.current_animation.count += 1
        self.current_animation.timer -= self.current_animation.animation_time

        if self.current_animation.count < self.current_animation.length:
            return
        if self.current_animation.loop:
            self.current_animation.count = 0
        else:
            self.current_animation.count -= 1
        self.on_repeat_animation()

    def offset_animation(self, value: float = 0):
        if value == 0:
            value = random() * self.current_animation.animation_time * self.current_animation.length
        self.current_animation.count = int(value % self.current_animation.length)
        self.current_animation.timer = value % self.current_animation.animation_time

    def get_texture(self) -> Texture:
        return self.atlas.textures[self.current_animation.start_index + self.current_animation.count]

    def get_surface(self) -> pygame.Surface:
        texture = self.get_texture()
        if self.flash_time > 0 and self.flash_time % self.flash_speed * 2 < self.flash_speed:
            return texture.get_flash_image(self.rotation)
        return texture.get_image(self.rotation)

    def is_animation_finished(self):
        if not self.current_animation.loop:
            return self.current_animation.count == self.current_animation.length - 1 and self.current_animation.timer >= 0

    def on_repeat_animation(self):
        if self.single_play:
            self.single_play = False
            self.update_animation_data(self.previous_animation)
