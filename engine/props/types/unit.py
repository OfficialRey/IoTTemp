from abc import ABC
from typing import List

import pygame

from engine.core.vector import Vector
from engine.graphics.animation.animation import AnimationType
from engine.graphics.atlas.animation import AnimationAtlas
from engine.props.bullet.bullet import Bullet, BulletType
from engine.props.types.collision import CollisionInformation
from engine.props.types.damageable import Damageable
from engine.props.types.sprite import Sprite
from engine.sound.game_sound import SoundEngine, GameSound
from engine.world.camera import Camera


class Unit(Damageable, ABC):

    def __init__(self, sound_engine: SoundEngine, atlas: AnimationAtlas, max_health: int, attack: int, defense: int,
                 max_speed: float = 0, acceleration: float = 0, center_position: Vector = Vector(),
                 velocity: Vector = Vector(), is_enemy: bool = True):
        super().__init__(atlas, max_health, attack, defense, max_speed, acceleration, center_position, velocity)
        self.sound_engine = sound_engine
        self.is_enemy = is_enemy
        self.triggered_death = False

    def update(self, world, delta_time: float):
        super().update(world, delta_time)
        self._death_update()
        if self.is_dead():
            return
        self.run_behaviour(world, delta_time)

    def _death_update(self):
        if self.is_dead() and not self.triggered_death:
            self.on_death()
            self.animation_manager.flash_time = 0
            self.triggered_death = True

    def register_bullet_hits(self, bullets: List[Bullet]):
        # Ensure bullets exist
        if len(bullets) == 0:
            return

        # Calculate collision and damage
        for bullet in bullets:
            if bullet.life_time > 0:
                collision_info = self.collide_generic(bullet)
                if collision_info.hit:
                    self.on_generic_collision(bullet, collision_info)
                    continue

    def on_generic_collision(self, other: Sprite, collision_info: CollisionInformation):
        self.on_collision(other, collision_info)

        # Bullet Hits
        if isinstance(other, Bullet):
            if other.owner.is_enemy is not self.is_enemy:
                self.damage(other.get_attack(), collision_info)
                other.life_time = 0
                self.on_hit()

    def play_sound(self, sound: GameSound):
        self.sound_engine.play_sound(sound)

    def run_behaviour(self, world, delta_time: float):
        raise NotImplementedError("Must implement generic behaviour")

    def on_hit(self):
        self.play_sound(GameSound.HURT)

    def on_death(self):
        self.play_sound(GameSound.DEATH)

    def on_attack(self):
        raise NotImplementedError("Must implement on_attack behaviour")

    def on_collision(self, other: Sprite, collision_info: CollisionInformation):
        raise NotImplementedError("Must implement collision behaviour")


class ShootingUnit(Unit, ABC):
    def __init__(self, sound_engine: SoundEngine, atlas: AnimationAtlas, bullet_type: BulletType, max_health: int,
                 attack: int, defense: int, max_speed: float, acceleration: float, shot_delay: float,
                 center_position: Vector = Vector(), velocity: Vector = Vector(), is_enemy: bool = True):
        super().__init__(sound_engine, atlas, max_health, attack, defense, max_speed, acceleration, center_position,
                         velocity,
                         is_enemy)
        self.bullet_type = bullet_type
        self.shot_delay = shot_delay
        self.current_shot_timer = 0
        self.bullets = []
        self.animation_manager.get_animation_data(AnimationType.RANGED_ATTACK).set_cycle_time(self.shot_delay)

    def shoot_bullet(self, direction: Vector) -> bool:
        if self.current_shot_timer >= self.shot_delay:
            bullet = Bullet(self, self.bullet_type, self.center_position, direction)
            self.bullets.append(bullet)
            self.current_shot_timer = 0
            self.sound_engine.play_sound(self.bullet_type.sound_type)
            return True
        return False

    def update(self, world, delta_time: float):
        super().update(world, delta_time)
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


class MeleeUnit(Unit, ABC):

    def __init__(self, sound_engine: SoundEngine, atlas: AnimationAtlas, max_health: int, attack: int, defense: int,
                 max_speed: float, acceleration: float, center_position: Vector = Vector(), velocity: Vector = Vector(),
                 is_enemy: bool = True):
        super().__init__(sound_engine, atlas, max_health, attack, defense, max_speed, acceleration, center_position,
                         velocity, is_enemy)
        self.melee_cooldown = 0
