from random import random

from engine.core.vector import Vector
from engine.props.player.player import Player
from engine.util.constants import FULL_ROTATION

MIN_DISTANCE = 100


class EnemyAI:

    def __init__(self, entity):
        self.entity = entity

    def run(self, world, delta_time: float):
        acceleration = Vector()
        # Keep distance to other units
        for unit in world.units.sprites():
            if isinstance(unit, Player):
                continue
            if unit == self.entity:
                continue

            me_to_unit: Vector = unit.center_position - self.entity.center_position
            distance = me_to_unit.magnitude()
            if distance < MIN_DISTANCE:
                acceleration += me_to_unit.normalize().inverse() * (MIN_DISTANCE / (distance + 0.00000001))

        self.entity.accelerate(acceleration, delta_time)

        # Execute specific ai
        self.run_ai(world, delta_time)

    def run_ai(self, world, delta_time: float):
        raise NotImplementedError()


class MeleeAI(EnemyAI):

    def __init__(self, entity):
        super().__init__(entity)

    def run_ai(self, world, delta_time: float):
        pass


class ShootingAI(EnemyAI):

    def __init__(self, entity, accuracy: float = 1, rounds: int = 1, round_delay: float = 0.5,
                 shot_delay: float = 1, target_distance: int = 700):
        super().__init__(entity)
        self.accuracy = accuracy
        self.rounds = rounds
        self.round_delay = round_delay
        self.shot_delay = shot_delay
        self.target_distance = target_distance

        self.shot_timer = 0
        self.round_timer = 0
        self.rounds_shot = 0

    def run_ai(self, world, delta_time: float):
        target = world.player
        vector = target.center_position - self.entity.center_position
        distance = vector.magnitude()

        acceleration = vector.normalize() * (distance - self.target_distance)
        self.entity.accelerate(acceleration, delta_time)
        self.shot_timer -= delta_time
        self.round_timer -= delta_time
        if self.shot_timer > 0 or self.round_timer > 0:
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

        # Create shots
        self.entity.shoot_bullet(vector.normalize())