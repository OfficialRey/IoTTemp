from engine.props.bullet.bullet import BulletType
from engine.sound.game_sound import SoundEngine


class Weapon:

    def __init__(self, name: str, bullet_type: BulletType):
        self.bullet_type = bullet_type

    def get_bullet_type(self):
        return self.bullet_type

    def get_sound(self, sound_engine: SoundEngine):
        return sound_engine.get_sound(self.bullet_type.get_sound_type())
