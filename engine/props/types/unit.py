from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.types.damageable import Damageable


class Unit(Damageable):

    def __init__(self, animation_atlas: AnimationAtlas, max_health: int, attack: int, defense: int,
                 max_speed: float = 0, acceleration: float = 0, position: Vector = Vector(),
                 velocity: Vector = Vector()):
        super().__init__(animation_atlas, max_health, attack, defense, max_speed, acceleration, position, velocity)

    def update(self, world, delta_time: float):
        self.act(world, delta_time)
        super().update(world, delta_time)

    def act(self, world, delta_time: float):
        raise NotImplementedError("Implement a behaviour for this prop!")