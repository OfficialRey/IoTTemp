from enum import Enum

from engine.core.vector import Vector, VECTOR_UP
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.types.entity import Entity


class BulletType(Enum):
    GENERIC = 0


class Bullet(Entity):

    def __init__(self, animation_atlas: AnimationAtlas, owner, bullet_type: BulletType,
                 position: Vector, velocity: Vector, max_speed: float = 0):
        super().__init__(animation_atlas, position, velocity, max_speed)
        self.owner = owner
        self.bullet_type = bullet_type
        self.life_time = 5
        self._rotate_texture()

    def _rotate_texture(self):
        # angle = self.velocity.normalize().angle(VECTOR_UP)
        pass

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        self.life_time -= delta_time
        if self.life_time > 0:
            return
