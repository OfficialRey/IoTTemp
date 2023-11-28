import pygame

from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.bullet.bullet import Bullet, BulletType
from engine.props.types.unit import Unit


class ShootingUnit(Unit):

    def __init__(self, animation_atlas: AnimationAtlas, max_health: int, attack: int, defense: int,
                 shot_delay: float, max_speed: float, acceleration: float, position: Vector = Vector(),
                 velocity: Vector = Vector()):
        super().__init__(animation_atlas, max_health, attack, defense, position, velocity, max_speed,
                         acceleration)
        self.shot_delay = shot_delay
        self.current_shot_timer = 0
        self.bullets = []

    def shoot_bullet(self, animation_atlas: AnimationAtlas, bullet_type: BulletType, direction: Vector):
        if self.current_shot_timer >= self.shot_delay:
            bullet = Bullet(animation_atlas, self, bullet_type, self.position, direction)
            self.bullets.append(bullet)
            self.current_shot_timer = 0

    def act(self, delta_time: float):
        if self.current_shot_timer >= self.shot_delay:
            return
        self.current_shot_timer += delta_time

    def render(self, surface: pygame.Surface, screen_position: Vector) -> None:
        super().render(surface, screen_position)
        for bullet in self.bullets:
            bullet.render()