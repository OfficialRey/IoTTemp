from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.entity import Sprite, Entity


class Bullet(Sprite):

    def __init__(self, animation_atlas: AnimationAtlas, owner: Entity, position: Vector, velocity: Vector,
                 max_speed: float = 0):
        super().__init__(animation_atlas, position, velocity, max_speed)
        self.owner = owner
