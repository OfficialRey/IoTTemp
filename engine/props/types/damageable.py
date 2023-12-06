from engine.core.vector import Vector
from engine.graphics.animation.animation import AnimationType
from engine.graphics.atlas.animation import AnimationAtlas
from engine.props.types.collision import CollisionInformation
from engine.props.types.sprite import Sprite

FLASH_TIME = 0.2


class Damageable(Sprite):

    def __init__(self, atlas: AnimationAtlas, max_health: int, attack: int, defense: int,
                 max_speed: float = 0, acceleration: float = 0, center_position: Vector = Vector(),
                 velocity: Vector = Vector()):
        super().__init__(atlas, max_speed, acceleration, center_position, velocity)
        self.max_health = max_health
        self.health = self.max_health
        self.attack = attack
        self.defense = defense

    def apply_knock_back(self, direction: Vector, strength: float):
        self.accelerate(direction.normalize(), strength)

    def damage(self, value: float, collision_info: CollisionInformation, knock_back_strength: float = 0.15):
        self.damage_true(value * self.get_damage_multiplier())
        if collision_info is not None:
            self.apply_knock_back(collision_info.direction.inverse(), knock_back_strength)

    def damage_true(self, value: float):
        self.health -= value
        self.flash_image(FLASH_TIME)

        if self.health <= 0:
            self.play_death_animation()

    def play_death_animation(self):
        self.animation_manager.update_animation_type(AnimationType.DEATH)
        self.animation_manager.loop = False
        self.animation_manager.timer = -2
        self.acceleration = 0
        self.velocity = Vector(0, 0)

    def collide_generic(self, other) -> CollisionInformation:
        if self.is_dead():
            return CollisionInformation()
        return super().collide_generic(other)

    def get_damage_multiplier(self):
        return 100 / (100 + self.defense)

    def is_dead(self) -> bool:
        return self.health <= 0

    def can_remove(self) -> bool:
        if not self.is_dead():
            return False
        if self.atlas.get_animation_data(AnimationType.DEATH) is not None:
            return self.animation_manager.is_animation_finished()
        return True
