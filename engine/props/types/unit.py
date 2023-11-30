from typing import List

import pygame

from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.bullet.bullet import Bullet
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

    def collides_with(self, other) -> bool:
        distance = self.get_center_position().distance(other.get_center_position())
        collision_radius = max(self.get_collision_radius(), other.get_collision_radius())
        print(distance)
        print(collision_radius)
        return distance <= collision_radius

    def register_bullet_hits(self, bullets: List[Bullet]):
        # Ensure bullets exist
        if len(bullets) == 0:
            return

        # Calculate collision and damage
        for bullet in bullets:
            if bullet.life_time >= 0:
                if self.collides_with(bullet):
                    self.damage(bullet.bullet_type.get_damage())
