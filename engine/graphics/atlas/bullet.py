from typing import List

from engine.core.vector import Vector
from engine.graphics.animation.animation import AnimationType, AnimationData
from engine.graphics.atlas.atlas import Atlas
from engine.graphics.textures.texture import Texture
from engine.props.bullet.bullet import BulletType
from engine.util.debug import print_debug


class BulletAtlas(Atlas):

    def __init__(self, path: str, file_name: str, sprite_width: int, sprite_height: int,
                 animation_time: float = 0.2, loop: bool = True, rotation_precision: int = 10):
        super().__init__(path, file_name, sprite_width, sprite_height, rotation_precision)

        print_debug(f"Creating bullet atlas {path}/{file_name}")

        self.animation_time = animation_time
        self.loop = loop
        self.rotation_precision = rotation_precision

        self.textures: List[Texture] = []
        self.animation_data: List[AnimationData] = []

        self._initialise()

    def _initialise(self):
        self._load_textures()

    def _load_textures(self):
        for i in range(self.y_length):
            surface = self.surface.subsurface(
                (0, i * self.sprite_height, self.surface.get_width(), self.sprite_height))
            textures = self._split_row(surface)
            animation_data = AnimationData(AnimationType.GENERIC, len(self.textures),
                                           len(self.textures) + len(textures),
                                           self.animation_time, self.loop)

            self.textures.extend(textures)
            self.animation_data.append(animation_data)

    def scale_textures(self, bullet_type: BulletType):
        animation_data = self.animation_data[bullet_type.animation_index]
        for i in range(animation_data.start_index, animation_data.end_index):
            self.textures[i].scale_texture(Vector(bullet_type.size, bullet_type.size))

    def get_animation_data(self, index: int):
        return self.animation_data[index]
