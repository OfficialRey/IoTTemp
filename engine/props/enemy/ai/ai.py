from random import random

from engine.core.vector import Vector
from engine.graphics.animation.animation import AnimationType
from engine.props.enemy.ai.path_finding.path import Path
from engine.props.enemy.enemy import ShootingEnemy, MeleeEnemy
from engine.props.player.player import Player
from engine.props.types.unit import Unit
from engine.util.constants import FULL_ROTATION

MIN_UNIT_DISTANCE = 100
UNIT_DISTANCING_FACTOR = 0.1


class EnemyAI:

    def __init__(self, entity):
        self.entity = entity

    def run(self, world, delta_time: float):
        # Execute specific ai
        self._run_ai(world, delta_time)

    def walk_to_player(self, world, delta_time: float):
        target = world.player
        path = Path(world, self.entity.center_position, target.center_position)
        target_direction = path.get_target_direction(self.entity)
        self.entity.accelerate_normalized(target_direction, delta_time)

    def space_units(self, world, delta_time: float):
        for unit in world.units.sprites():
            if isinstance(unit, Player):
                continue
            if unit is self.entity:
                continue

            vector = self.entity.center_position - unit.center_position
            distance = vector.magnitude()

            if distance < MIN_UNIT_DISTANCE:
                self.entity.accelerate_uncapped(vector.normalize() * delta_time * UNIT_DISTANCING_FACTOR)

    def _run_ai(self, world, delta_time: float):
        raise NotImplementedError()


class MeleeAI(EnemyAI):

    def __init__(self, entity: MeleeEnemy, attack_cooldown: float = 3, attack_distance: float = 500,
                 attack_acceleration: int = 3000):
        super().__init__(entity)
        self.attack_cooldown = attack_cooldown
        self.attack_distance = attack_distance
        self.attack_acceleration = attack_acceleration

        self.attack_timer = 0

    def _run_ai(self, world, delta_time: float):
        self.walk_to_player(world, delta_time)

        target = world.player
        self._attack_unit(target, delta_time)

    def _attack_unit(self, target: Unit, delta_time: float):
        if self.attack_timer > 0:
            self.attack_timer -= delta_time
            return

        vector = target.center_position - self.entity.center_position
        distance = vector.magnitude()

        return
        if distance < self.attack_distance:
            self.entity.accelerate_uncapped(vector * self.attack_acceleration)
            self.attack_timer = self.attack_cooldown


class ShootingAI(EnemyAI):

    def __init__(self, entity: ShootingEnemy, accuracy: float = 0.95, rounds: int = 3, round_delay: float = 0.2,
                 shot_delay: float = 3, target_distance: int = 400):
        super().__init__(entity)
        self.accuracy = accuracy
        self.rounds = rounds
        self.round_delay = round_delay
        self.shot_delay = shot_delay
        self.target_distance = target_distance

        self.shot_timer = self.shot_delay
        self.round_timer = self.round_delay
        self.rounds_shot = 0

        self.entity.shot_delay = 0
        self.entity.animation_manager.get_animation_data(AnimationType.RANGED_ATTACK_E).set_cycle_time(self.round_delay)
        self.entity.animation_manager.get_animation_data(AnimationType.RANGED_ATTACK_W).set_cycle_time(self.round_delay)

    def _run_ai(self, world, delta_time: float):
        me_to_player: Vector = world.player.center_position - self.entity.center_position
        if me_to_player.magnitude() > self.target_distance:
            self.walk_to_player(world, delta_time)
        else:
            self.entity.accelerate_normalized(me_to_player.inverse())

        self.shot_timer -= delta_time
        self.round_timer -= delta_time
        if self.shot_timer <= 0 and self.round_timer <= 0:
            self.shoot(world)

    def reset_shooting(self):
        self.shot_timer = self.shot_delay
        self.round_timer = self.round_delay
        self.rounds_shot = 0

    def shoot(self, world):
        if self.rounds_shot >= self.rounds:
            self.reset_shooting()
            return

        angle_offset = (-(1 - self.accuracy) + 2 * random() * (1 - self.accuracy)) * FULL_ROTATION
        target = world.player
        vector = target.center_position - self.entity.center_position
        vector = vector.rotate_counter_clockwise(angle_offset)

        animation_type = AnimationType.RANGED_ATTACK_W if vector.x < 0 else AnimationType.RANGED_ATTACK_E

        self.entity.velocity = Vector()
        self.entity.animation_manager.single_play_animation(animation_type)
        self.entity.shoot_bullet(vector.normalize())
        self.round_timer = self.round_delay
        self.rounds_shot += 1
