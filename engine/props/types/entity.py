from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.types.sprite import Sprite


class Entity(Sprite):

    def __init__(self, animation_atlas: AnimationAtlas, max_speed: float = 0, acceleration: float = 0,
                 position: Vector = Vector(),
                 velocity: Vector = Vector()):
        super().__init__(animation_atlas, max_speed, acceleration, position, velocity)
