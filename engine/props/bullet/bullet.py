import math

from enum import Enum

from engine.core.vector import Vector
from engine.graphics.atlas.atlas import Atlas
from engine.props.types.sprite import Sprite
from engine.sound.game_sound import GameSound


class BulletType(Enum):
    # Speed, Animation, Rotation Offset, Size, Damage, GameSound
    LASER = (8000, 15, 90, 1, 1, GameSound.LASER)

    def get_speed(self):
        return self.value[0]

    def get_animation(self):
        return self.value[1]

    def get_rotation_offset(self):
        return self.value[2]

    def get_size(self):
        return self.value[3]

    def get_attack(self):
        return self.value[4]

    def get_sound_type(self):
        return self.value[5]


class Bullet(Sprite):

    def __init__(self, atlas: Atlas, owner, bullet_type: BulletType,
                 center_position: Vector, velocity: Vector, max_speed: float = 0):
        super().__init__(atlas, max_speed, 0, center_position, velocity)
        self.owner = owner
        self.max_speed = bullet_type.value[0]
        self.velocity = self.velocity.normalize() * self.max_speed
        self.bullet_type = bullet_type
        self.life_time = 5
        self.animation_manager.update_animation_data(atlas.get_animation_data(self.bullet_type))
        self.set_rotation(self.bullet_type.get_rotation_offset() - self.get_velocity_rotation())

    def update(self, world, delta_time: float) -> None:
        super().update(world, delta_time)

        self.life_time -= delta_time

    def fix_rotation(self):
        vector = Vector(self.velocity.x, -self.velocity.y).normalize()
        angle = math.degrees(math.atan2(*vector.as_tuple()))
        self.set_rotation(self.bullet_type.get_rotation_offset() - angle)

    def get_attack(self):
        return self.owner.attack + self.bullet_type.get_attack()
