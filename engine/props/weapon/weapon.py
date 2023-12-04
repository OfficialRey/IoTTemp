from enum import Enum

from engine.graphics.atlas.animation import AnimationAtlas
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.bullet.bullet import BulletType
from engine.sound.game_sound import SoundEngine


class WeaponTypes(Enum):
    # Format: Name, BulletType
    LASER_GUN = ("Laser Gun", BulletType.LASER)


class Weapon:

    def __init__(self, name: str, animation_atlas: AnimationAtlas, bullet_type: BulletType):
        self.name = name
        self.animation_atlas = animation_atlas
        self.animation_atlas.set_scale(bullet_type.get_size())
        self.bullet_type = bullet_type

    def get_bullet_type(self):
        return self.bullet_type

    def get_sound(self, sound_engine: SoundEngine):
        return sound_engine.get_sound(self.bullet_type.get_sound_type())


class WeaponManager:

    def __init__(self, texture_manager: TextureManager):
        self.laser_gun = Weapon("Laser Gun", texture_manager.bullets, BulletType.LASER)
