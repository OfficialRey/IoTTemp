from typing import List, Tuple

from engine.graphics.animation.animation import AnimationType, AnimationData
from engine.graphics.atlas.atlas import Atlas
from engine.graphics.textures.texture import Texture
from engine.util.debug import print_debug

MIRROR_ANIMATIONS = {
    AnimationType.WALKING_N: AnimationType.WALKING_S,
    AnimationType.WALKING_E: AnimationType.WALKING_W,
    AnimationType.WALKING_S: AnimationType.WALKING_N,
    AnimationType.WALKING_W: AnimationType.WALKING_E,

    AnimationType.RANGED_ATTACK_E: AnimationType.RANGED_ATTACK_W,
    AnimationType.RANGED_ATTACK_W: AnimationType.RANGED_ATTACK_E
}


class AnimationAtlas(Atlas):

    def __init__(self, path: str, file_name: str, animation_types: List[AnimationType],
                 sprite_width: int, sprite_height: int, animation_time: float = 0.2, loop: bool = True,
                 rotation_precision: int = 360):
        super().__init__(path, file_name, sprite_width, sprite_height)

        print_debug(f"Creating animation atlas {path}/{file_name}")

        self.animation_types = animation_types
        self.animation_time = animation_time
        self.loop = loop
        self.rotation_precision = rotation_precision

        self.textures: List[Texture] = []
        self.animation_data: List[AnimationData] = []

        self._load_textures()

    def _load_textures(self):
        self.textures = []

        for i in range(len(self.animation_types)):
            animation_type = self.animation_types[i]
            if animation_type is not None:
                surface = self.surface.subsurface(
                    (0, i * self.sprite_height, self.surface.get_width(), self.sprite_height))
                textures = self._split_row(surface)
                animation_data = AnimationData(animation_type, len(self.textures), len(self.textures) + len(textures),
                                               self.animation_time, self.loop)
                self.textures.extend(textures)
                self.animation_data.append(animation_data)

                # Mirror animations
                for key in MIRROR_ANIMATIONS.keys():
                    if animation_type == key and MIRROR_ANIMATIONS[key] not in self.animation_types:
                        new_textures, new_animation_data = self._mirror_animation(textures, MIRROR_ANIMATIONS[key])
                        self.textures.extend(new_textures)
                        self.animation_data.append(new_animation_data)

    def _mirror_animation(self, textures, animation_type) -> Tuple[List[Texture], AnimationData]:
        new_textures = []
        for texture in textures:
            new_texture = Texture(texture.base_image.copy(), texture.rotation_precision)
            new_texture.mirror_texture(True)
            new_textures.append(new_texture)
        new_animation_data = AnimationData(animation_type, len(self.textures), len(self.textures) + len(textures),
                                           self.animation_time, self.loop)
        return new_textures, new_animation_data

    def get_animation_data(self, animation_type: AnimationType):
        for animation_data in self.animation_data:
            if animation_data.animation_type == animation_type:
                return animation_data
        return None

    def get_size(self):
        return self.sprite_width, self.sprite_height

    def _get_animation_types(self):
        return [data.animation_type for data in self.animation_data]
