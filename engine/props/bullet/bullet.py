from enum import Enum

from engine.core.vector import Vector, VECTOR_UP
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.types.entity import Sprite, Entity


class BulletType(Enum):
    GENERIC = 0


class Bullet(Sprite):

    def __init__(self, animation_atlas: AnimationAtlas, owner: Entity, position: Vector, velocity: Vector,
                 max_speed: float = 0):
        super().__init__(animation_atlas, position, velocity, max_speed)
        self.owner = owner
        self._rotate_texture()
        self.life_time = 5

    def _rotate_texture(self):
        angle = self.velocity.normalize().angle(VECTOR_UP)

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        self.life_time -= delta_time
        if self.life_time <= 0:
            # TODO: Delete object
            pass
