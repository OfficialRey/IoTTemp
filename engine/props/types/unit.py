from abc import ABC
from random import choice, random
from typing import List

import pygame

from engine.core.vector import Vector
from engine.graphics.animation.animation import AnimationType
from engine.graphics.atlas.animation import AnimationAtlas
from engine.props.bullet.bullet import Bullet, BulletType
from engine.props.data import UnitData
from engine.props.types.damageable import Damageable
from engine.props.types.sprite import Sprite
from engine.sound.game_sound import SoundMixer, GameSound
from engine.world.camera import Camera
from engine.world.collision import CollisionInformation

AMBIENCE_TIME = 5  # Play every 3 seconds


class Unit(Damageable, ABC):

    def __init__(self, sound_mixer: SoundMixer, atlas: AnimationAtlas, world, ambience: List[GameSound],
                 max_health: int, attack: int,
                 defense: int, max_speed: float = 0, acceleration: float = 0, center_position: Vector = Vector(),
                 velocity: Vector = Vector(), is_enemy: bool = True):
        super().__init__(sound_mixer, atlas, world, max_health, attack, defense, max_speed, acceleration,
                         center_position, velocity)
        self.ambience = ambience
        self.is_enemy = is_enemy
        self.triggered_death = False

    def update_unit_data(self, data: UnitData):
        self.max_health = data.get_health()
        self.attack = data.get_attack()
        self.defense = data.get_defense()
        self.max_speed = data.get_max_speed()
        self.acceleration = data.get_acceleration()

    def update(self, world, delta_time: float):
        super().update(world, delta_time)
        if self.is_dead():
            return
        self.run_behaviour(world, delta_time)
        self.play_ambience(world, delta_time)

    def register_bullet_hits(self, bullets: List[Bullet]):
        # Ensure bullets exist
        if len(bullets) == 0:
            return

        # Calculate collision and damage
        for bullet in bullets:
            if bullet.life_time > 0:
                self.register_bullet_damage(bullet)

    def register_melee_hits(self, units: List):
        for unit in units:
            if unit is not self:
                if unit.is_enemy and not self.is_enemy:  # Only enemies can melee damage
                    self.register_melee_damage(unit)

    def register_bullet_damage(self, bullet):
        collision_info = self.collide_generic(bullet)
        if collision_info.hit:
            # Bullet Hits
            if isinstance(bullet, Bullet):
                if bullet.owner.is_enemy is not self.is_enemy:
                    self.damage(bullet.get_attack(), collision_info)
                    bullet.life_time = 0
                    self.on_hit()

    def register_melee_damage(self, unit):
        collision_info = self.collision.collides_with(unit.collision)
        if collision_info.hit:
            self.damage(unit.attack, collision_info, melee_damage=True)
            self.on_hit()

    def on_generic_collision(self, other: Sprite, collision_info: CollisionInformation):
        self.on_collision(other, collision_info)

        # Bullet Hits
        if isinstance(other, Bullet):
            if other.owner.is_enemy is not self.is_enemy:
                self.damage(other.get_attack(), collision_info)
                other.life_time = 0
                self.on_hit()

    def play_ambience(self, world, delta_time: float):
        if len(self.ambience) == 0:
            return

        if random() > delta_time / AMBIENCE_TIME:
            return
        sound = choice(self.ambience)
        self.sound_mixer.play_positioned_sound(sound, world, self.center_position)

    def run_behaviour(self, world, delta_time: float):
        raise NotImplementedError("Must implement generic behaviour")

    def on_death(self):
        self.sound_mixer.play_positioned_sound(GameSound.DEATH, self.world, self.center_position)
        super().on_death()

    def on_attack(self):
        raise NotImplementedError("Must implement on_attack behaviour")

    def on_collision(self, other: Sprite, collision_info: CollisionInformation):
        raise NotImplementedError("Must implement collision behaviour")


class ShootingUnit(Unit, ABC):
    def __init__(self, sound_mixer: SoundMixer, atlas: AnimationAtlas, world, ambience: List[GameSound],
                 bullet_type: BulletType, max_health: int,
                 attack: int, defense: int, max_speed: float, acceleration: float, shot_delay: float,
                 center_position: Vector = Vector(), velocity: Vector = Vector(), is_enemy: bool = True):
        super().__init__(sound_mixer, atlas, world, ambience, max_health, attack, defense, max_speed, acceleration,
                         center_position, velocity, is_enemy)
        self.bullet_type = bullet_type
        self.shot_delay = shot_delay
        self.current_shot_timer = 0
        self.bullets = []
        self.animation_manager.get_animation_data(AnimationType.RANGED_ATTACK_E).set_cycle_time(self.shot_delay)
        self.animation_manager.get_animation_data(AnimationType.RANGED_ATTACK_W).set_cycle_time(self.shot_delay)

    def update_unit_data(self, data: UnitData):
        super().update_unit_data(data)
        self.shot_delay = data.get_shot_delay()

    def shoot_bullet(self, direction: Vector) -> bool:
        if self.is_dead():
            return False
        if self.current_shot_timer < self.shot_delay:
            return False

        bullet = Bullet(self, self.bullet_type, self.center_position, direction)
        self.bullets.append(bullet)
        self.current_shot_timer = 0
        self.sound_mixer.play_sound(self.bullet_type.sound_type,
                                    self.center_position - self.world.player.center_position)
        return True

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

    def __init__(self, sound_mixer: SoundMixer, atlas: AnimationAtlas, world, ambience: List[GameSound],
                 max_health: int, attack: int, defense: int, max_speed: float, acceleration: float,
                 center_position: Vector = Vector(), velocity: Vector = Vector(), is_enemy: bool = True):
        super().__init__(sound_mixer, atlas, world, ambience, max_health, attack, defense, max_speed, acceleration,
                         center_position, velocity, is_enemy)
        self.melee_cooldown = 0
