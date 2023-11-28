from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.types.entity import Entity


class Damageable(Entity):

    def __init__(self, world, animation_atlas: AnimationAtlas, max_health: int, attack: int, defense: int,
                 position: Vector = Vector(), velocity: Vector = Vector(), max_speed: float = 0,
                 acceleration: float = 0):
        super().__init__(world, animation_atlas, position, velocity, max_speed, acceleration)
        self.max_health = max_health
        self.health = self.max_health
        self.attack = attack
        self.defense = defense

    def _act(self, delta_time: float) -> None:
        pass

    def damage(self, value: float):
        self.damage_true(value * self.get_damage_multiplier())

    def damage_true(self, value: float):
        self.health -= value

    def get_damage_multiplier(self):
        return 100 / (100 + self.defense)
