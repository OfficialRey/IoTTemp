from typing import List

import pygame

from engine.core.vector import Vector
from engine.graphics.animation.animation import AnimationType, AnimationData
from engine.graphics.atlas.atlas import Atlas
from engine.graphics.textures.texture import Texture
from engine.props.bullet.bullet import BulletType
from engine.util.debug import print_debug


class BulletAtlas(Atlas):

    def __init__(self, path: str, file_name: str, sprite_width: int, sprite_height: int, bullet_types: List[BulletType],
                 animation_time: float = 0.2, loop: bool = True, rotation_precision: int = 10):
        super().__init__(path, file_name, sprite_width, sprite_height)

        print_debug(f"Creating bullet atlas {path}/{file_name}")

        self.animation_time = animation_time
        self.loop = loop
        self.rotation_precision = rotation_precision

        self.bullet_types = bullet_types
        self.textures: List[Texture] = []
        self.animation_data: List[AnimationData] = []

        self._initialise()

    def _initialise(self):
        self._load_textures()
        self._scale_textures()

    def _load_textures(self):

        for bullet_type in self.bullet_types:
            surface = self.surface.subsurface(
                (0, bullet_type.get_animation() * self.sprite_height, self.surface.get_width(), self.sprite_height))
            textures = self._split_row(surface)
            animation_data = AnimationData(AnimationType.GENERIC, len(self.textures),
                                           len(self.textures) + len(textures),
                                           self.animation_time, self.loop)

            self.textures.extend(textures)
            self.animation_data.append(animation_data)

    def _split_row(self, surface: pygame.Surface) -> List[Texture]:
        textures = []
        for x in range(surface.get_width() // self.sprite_width):
            texture = Texture(
                surface.subsurface((x * self.sprite_width, 0, self.sprite_width, self.sprite_height)),
                rotation_precision=self.rotation_precision)
            if not texture.is_empty():
                textures.append(texture)
        return textures

    def _scale_textures(self):
        for animation_data in self.animation_data:
            for i in range(animation_data.start_index, animation_data.stop_index):
                index = self.animation_data.index(animation_data)
                size = self.bullet_types[index].get_size()
                self.textures[i].scale_texture(Vector(size, size))

    def get_animation_data(self, bullet_type: BulletType):
        index = self.bullet_types.index(bullet_type)
        return self.animation_data[index]
