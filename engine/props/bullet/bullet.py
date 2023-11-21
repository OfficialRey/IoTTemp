from engine.core.vector import Vector, VECTOR_UP
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.entity import Sprite, Entity


class Bullet(Sprite):

    def __init__(self, animation_atlas: AnimationAtlas, owner: Entity, position: Vector, velocity: Vector,
                 max_speed: float = 0):
        super().__init__(animation_atlas, position, velocity, max_speed)
        self.owner = owner
        self._rotate_texture()

    def _rotate_texture(self):
        angle = self.velocity.normalize().angle(VECTOR_UP)
