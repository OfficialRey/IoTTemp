from typing import List

import pygame

from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.bullet.bullet import Bullet, BulletType
from engine.props.types.unit import Unit
from engine.world.camera import Camera


class ShootingUnit(Unit):

    def __init__(self, animation_atlas: AnimationAtlas, bullet_atlas: AnimationAtlas, max_health: int, attack: int,
                 defense: int, shot_delay: float, max_speed: float, acceleration: float, position: Vector = Vector(),
                 velocity: Vector = Vector()):
        super().__init__(animation_atlas, max_health, attack, defense, max_speed, acceleration, position, velocity)
        self.bullet_atlas = bullet_atlas
        self.shot_delay = shot_delay
        self.current_shot_timer = 0
        self.bullets = []

    def shoot_bullet(self, bullet_type: BulletType, direction: Vector) -> bool:
        if self.current_shot_timer >= self.shot_delay:
            bullet = Bullet(self.bullet_atlas, self, bullet_type, self.position, direction)
            self.bullets.append(bullet)
            self.current_shot_timer = 0
            return True
        return False

    def act(self, world, delta_time: float):
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

    def set_size(self, width: int, height: int):
        super().set_size(width, height)

    def get_bullets(self) -> List[Bullet]:
        return self.bullets
