from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.types.damageable import Damageable


class Unit(Damageable):

    def __init__(self, animation_atlas: AnimationAtlas, max_health: int, attack: int, defense: int,
                 position: Vector = Vector(), velocity: Vector = Vector(),
                 max_speed: float = 0, acceleration: float = 0):
        super().__init__(animation_atlas, max_health, attack, defense, position, velocity, max_speed, acceleration)

    def update(self, delta_time: float):
        self.act(delta_time)
        super().update(delta_time)

    def act(self, delta_time: float):
        raise NotImplementedError("Implement a behaviour for this prop!")
