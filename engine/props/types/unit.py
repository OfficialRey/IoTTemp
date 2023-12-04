from abc import ABC
from typing import List

import pygame

from engine.core.vector import Vector
from engine.graphics.atlas.animation import AnimationAtlas
from engine.props.bullet.bullet import Bullet, BulletType
from engine.props.types.collision import CollisionInformation
from engine.props.types.damageable import Damageable
from engine.props.types.sprite import Sprite
from engine.props.weapon.weapon import Weapon
from engine.world.camera import Camera


class Unit(Damageable):

    def __init__(self, atlas: AnimationAtlas, max_health: int, attack: int, defense: int,
                 max_speed: float = 0, acceleration: float = 0, center_position: Vector = Vector(),
                 velocity: Vector = Vector()):
        super().__init__(atlas, max_health, attack, defense, max_speed, acceleration, center_position, velocity)

    def update(self, world, delta_time: float):
        self.run_behaviour(world, delta_time)
        self._unit_update()
        super().update(world, delta_time)

    def _unit_update(self):
        if self.is_dead():
            self.on_death()

    def register_bullet_hits(self, bullets: List[Bullet]):
        # Ensure bullets exist
        if len(bullets) == 0:
            return

        # Calculate collision and damage
        for bullet in bullets:
            if bullet.life_time > 0:
                collision_info = self.collide_generic(bullet)
                if collision_info.hit:
                    self.on_collision(bullet, collision_info)
                    continue

    def is_dead(self):
        return self.health <= 0

    def run_behaviour(self, world, delta_time: float):
        raise NotImplementedError("Must implement generic behaviour")

    def on_hit(self):
        raise NotImplementedError("Must implement on_hit behaviour")

    def on_death(self):
        raise NotImplementedError("Must implement on_death behaviour")

    def on_attack(self):
        raise NotImplementedError("Must implement on_attack behaviour")

    def on_collision(self, other: Sprite, collision_info: CollisionInformation):
        raise NotImplementedError("Must implement collision behaviour")


class ShootingUnit(Unit, ABC):
    def __init__(self, atlas: AnimationAtlas, weapon: Weapon, max_health: int, attack: int,
                 defense: int, shot_delay: float, max_speed: float, acceleration: float,
                 center_position: Vector = Vector(),
                 velocity: Vector = Vector()):
        super().__init__(atlas, max_health, attack, defense, max_speed, acceleration, center_position, velocity)
        self.weapon = weapon
        self.shot_delay = shot_delay
        self.current_shot_timer = 0
        self.bullets = []

    def shoot_bullet(self, bullet_type: BulletType, direction: Vector) -> bool:
        if self.current_shot_timer >= self.shot_delay:
            bullet = Bullet(self.weapon.animation_atlas, self, bullet_type, self.center_position, direction)
            self.bullets.append(bullet)
            self.current_shot_timer = 0
            return True
        return False

    def run_behaviour(self, world, delta_time: float):
        for bullet in self.bullets:
            bullet.update(world, delta_time)
            if bullet.life_time <= 0:
                self.bullets.remove(bullet)

        # Allow Auto Fire
        if self.current_shot_timer >= self.shot_delay:
            return
        self.current_shot_timer += delta_time

    def render(self, surface: pygame.Surface, camera: Camera) -> None:
        for bullet in self.bullets:
            bullet.render(surface, camera)
        super().render(surface, camera)

    def get_bullets(self) -> List[Bullet]:
        return self.bullets
