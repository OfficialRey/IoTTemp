from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.types.entity import Entity

FLASH_TIME = 0.5


class Damageable(Entity):

    def __init__(self, animation_atlas: AnimationAtlas, max_health: int, attack: int, defense: int,
                 max_speed: float = 0, acceleration: float = 0, position: Vector = Vector(),
                 velocity: Vector = Vector()):
        super().__init__(animation_atlas, max_speed, acceleration, position, velocity)
        self.max_health = max_health
        self.health = self.max_health
        self.attack = attack
        self.defense = defense

    def damage(self, value: float):
        self.damage_true(value * self.get_damage_multiplier())

    def damage_true(self, value: float):
        self.health -= value
        self.flash(FLASH_TIME)

    def get_damage_multiplier(self):
        return 100 / (100 + self.defense)
