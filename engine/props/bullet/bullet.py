import math

from engine.core.vector import Vector
from engine.props.types.sprite import Sprite
from engine.sound.game_sound import GameSound


class BulletType:

    def __init__(self, atlas, animation_index: int, speed: int, rotation_offset: int, size: float,
                 attack: int, sound_type: GameSound):
        self.atlas = atlas
        self.animation_index = animation_index
        self.speed = speed
        self.rotation_offset = rotation_offset
        self.size = size
        self.attack = attack
        self.sound_type = sound_type


class BulletManager:

    def __init__(self, bullet_atlas):
        self.atlas = bullet_atlas
        self.laser = BulletType(bullet_atlas, 16, 8000, 90, 5, 10, GameSound.LASER)

        self.bullets = [
            self.laser
        ]

        self.scale_bullets()

    def scale_bullets(self):
        for bullet in self.bullets:
            self.atlas.scale_textures(bullet)


class Bullet(Sprite):

    def __init__(self, owner, bullet_type: BulletType, center_position: Vector, direction: Vector):
        super().__init__(bullet_type.atlas, bullet_type.speed, 0, center_position, direction)
        self.owner = owner
        self.velocity = self.velocity.normalize() * self.max_speed
        self.bullet_type = bullet_type
        self.life_time = 5
        self.animation_manager.update_animation_data(
            self.atlas.get_animation_data(self.bullet_type.animation_index))
        self.set_rotation(self.bullet_type.rotation_offset - self.get_velocity_rotation())

    def update(self, world, delta_time: float) -> None:
        super().update(world, delta_time)

        self.life_time -= delta_time

    def fix_rotation(self):
        vector = Vector(self.velocity.x, -self.velocity.y).normalize()
        angle = math.degrees(math.atan2(*vector.as_tuple()))
        self.set_rotation(self.bullet_type.rotation_offset - angle)

    def get_attack(self):
        return self.owner.attack + self.bullet_type.attack
