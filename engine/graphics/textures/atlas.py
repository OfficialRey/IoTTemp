import os.path
from typing import List, Tuple, Union

import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture import Texture
from engine.graphics.textures.texture_animation import AnimationType, TextureAnimation
from engine.util.debug import print_debug
from engine.util.resources import get_resource_path


class LevelAtlas:

    def __init__(self, path: str, file_name: str, sprite_width: int, sprite_height: int):
        print_debug(f"Creating level atlas {path}/{file_name}")
        self.image = pygame.image.load(os.path.join(get_resource_path(), os.path.join(path, file_name))).convert_alpha()
        self.path = path
        self.file_name = file_name

        self.base_width = sprite_width
        self.base_height = sprite_height

        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.atlas_width = self.image.get_width()
        self.atlas_height = self.image.get_height()
        self.x_length = self.atlas_width // self.sprite_width
        self.y_length = self.atlas_height // self.sprite_height
        self.count = self.x_length * self.y_length

        self.textures = self._load_sheet()

    def set_scale(self, scale: Vector):
        for texture in self.textures:
            texture.set_scale(scale)
        texture = self.textures[0]
        self.sprite_width, self.sprite_height = texture.image.get_size()

    def set_size(self, width: int, height: int):
        x_scale = width / self.base_width
        y_scale = height / self.base_height
        self.set_scale(Vector(x_scale, y_scale))

    def get_texture_size(self) -> Tuple[int, int]:
        return self.sprite_width, self.sprite_height

    def _load_sheet(self) -> List[Texture]:
        textures = []
        for y in range(self.y_length):
            for x in range(self.x_length):
                texture = Texture(self.image.subsurface(
                    (x * self.sprite_width, y * self.sprite_height, self.sprite_width, self.sprite_height)))
                if not texture.is_empty():
                    textures.append(texture)
        return textures

    def __getitem__(self, item: int) -> Texture:
        return self.textures[item].copy()


class AnimationAtlas:

    def __init__(self, path: str = None, file_name: str = None, animation_types: List[AnimationType] = None,
                 sprite_width: int = None, sprite_height: int = None, time: float = 0.2, loop: bool = True,
                 scale: Union[Vector, float] = 1, information: Tuple = None):
        if information is not None:
            # Format: animation_types, sprite_width, sprite_height, base_width, base_height, time, loop, texture_animations, scale
            self.animation_types = information[0]
            self.sprite_width = information[1]
            self.sprite_height = information[2]
            self.base_width = information[3]
            self.base_height = information[4]
            self.time = information[5]
            self.loop = information[6]
            self.texture_animations = [animation.copy() for animation in information[7]]
            self.scale = information[8]
        else:
            print_debug(f"Creating animation atlas {path}/{file_name}")
            self.path = path
            self.file_name = file_name
            self.surface = pygame.image.load(
                os.path.join(get_resource_path(), os.path.join(path, file_name))).convert_alpha()
            self.animation_types = animation_types
            self.sprite_width, self.sprite_height = sprite_width, sprite_height
            self.time = time
            self.loop = loop

            self.base_width = sprite_width
            self.base_height = sprite_height

            self.texture_animations = self._load_animations()
            self.scale = Vector(1, 1)
            self.set_scale(scale if isinstance(scale, Vector) else Vector(scale, scale))

    def _load_animations(self) -> List[TextureAnimation]:
        animations = []
        for i in range(len(self.animation_types)):
            animation_type = self.animation_types[i]
            if animation_type is not None:
                animations.append(
                    TextureAnimation(self.surface.subsurface((0, i * self.sprite_height, self.surface.get_width(),
                                                              self.sprite_height)),
                                     self.sprite_width, animation_type, self.time, self.loop))

        # Mirror walking animation
        # if AnimationType.WALKING_W not in self.animation_types and AnimationType.WALKING_E in self.animation_types:
        # Probably only east here. Expand to allow mirroring
        #            animation = animations[self.animation_types.index(AnimationType.WALKING_E)]
        #            animation = animation.copy()
        #            animation.mirror()
        #            animations.append(animation)

        return animations

    def set_scale(self, scale: Vector):
        self.scale = scale
        for texture_animation in self.texture_animations:
            texture_animation.set_scale(scale)

    def set_size(self, width: int, height: int):
        x_scale = width / self.base_width
        y_scale = height / self.base_height
        self.set_scale(Vector(x_scale, y_scale))

    def update(self, delta_time: float):
        for animation in self.texture_animations:
            animation.update(delta_time)

    def get_texture(self, index: AnimationType) -> Texture:
        return self.texture_animations[index.value].get_texture()

    def get_animation(self, animation_type: AnimationType):
        for animation in self.texture_animations:
            if animation.animation_type == animation_type:
                return animation
        return None

    def copy(self):
        # Format: animation_types, sprite_width, sprite_height, base_width, base_height, time, loop, texture_animations
        return AnimationAtlas(information=(
            self.animation_types, self.sprite_width, self.sprite_height, self.base_width, self.base_height, self.time,
            self.loop, self.texture_animations, self.scale))
