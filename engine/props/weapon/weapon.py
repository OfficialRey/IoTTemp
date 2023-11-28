from engine.props.types.entity import Sprite, Entity
from engine.world.world import World


class Weapon:

    def __init__(self, shot_speed: int, base_damage: int, projectile_sprite: Sprite):
        self.shot_speed = shot_speed
        self.base_damage = base_damage
        self.projectile_sprite = projectile_sprite

    def shoot(self, world: World, shooter: Entity):
        raise NotImplementedError("Not implemented")
