from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.types.sprite import Sprite


class Entity(Sprite):

    def __init__(self, world, animation_atlas: AnimationAtlas, position: Vector = Vector(),
                 velocity: Vector = Vector(), max_speed: float = 0, acceleration: float = 0):
        super().__init__(animation_atlas, position, velocity, max_speed, acceleration)
        self.world = world

    def update(self, delta_time: float):
        super().update(delta_time)
