from engine.props.bullet.bullet import BulletManager, BulletType
from engine.sound.game_sound import SoundMixer


class Weapon:

    def __init__(self, name: str, bullet_type: BulletType):
        self.name = name
        self.bullet_type = bullet_type

    def get_bullet_type(self):
        return self.bullet_type

    def get_sound(self, sound_mixer: SoundMixer):
        return sound_mixer.get_sound(self.bullet_type.sound_type)


class WeaponManager:

    def __init__(self, bullet_manager: BulletManager):
        self.laser_gun = Weapon("Laser Gun", bullet_manager.laser)
