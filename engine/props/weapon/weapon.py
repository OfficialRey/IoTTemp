from engine.props.bullet.bullet import BulletManager, BulletType
from engine.sound.game_sound import SoundMixer


class Weapon:

    def __init__(self, name: str, bullet_type: BulletType, shot_delay: float):
        self.name = name
        self.bullet_type = bullet_type
        self.shot_delay = shot_delay

    def get_sound(self, sound_mixer: SoundMixer):
        return sound_mixer.get_sound(self.bullet_type.sound_type)


class WeaponManager:

    def __init__(self, bullet_manager: BulletManager):
        self.laser_gun = Weapon("Laser Gun", bullet_manager.laser, 0.3)
        self.comet_gun = Weapon("Comet Gun", bullet_manager.comet, 0.1)
