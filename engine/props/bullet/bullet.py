from enum import Enum

from engine.core.vector import Vector, VECTOR_UP
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.types.entity import Entity


class BulletType(Enum):
    # Speed, Animation, Size
    GENERIC = (500, 12, 1)


class Bullet(Entity):

    def __init__(self, animation_atlas: AnimationAtlas, owner, bullet_type: BulletType,
                 position: Vector, velocity: Vector, max_speed: float = 0):
        super().__init__(animation_atlas, max_speed, 0, position, velocity)
        self.owner = owner
        self.max_speed = bullet_type.value[0]
        self.velocity = self.velocity.normalize() * self.max_speed
        self.bullet_type = bullet_type
        self.life_time = 5
        self._rotate_texture()
        self.play_animation(bullet_type.value[1])

    def update(self, world, delta_time: float) -> None:
        super().update(world, delta_time)

        self.life_time -= delta_time
        if self.life_time > 0:
            return
