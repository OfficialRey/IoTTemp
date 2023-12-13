from enum import IntEnum

from engine.core.vector import Vector
from engine.props.enemy.ai.ai import MeleeAI
from engine.props.enemy.ai.path_finding.path import Path
from engine.props.enemy.enemy import MeleeEnemy


class CentipedeState(IntEnum):
    HEAD = 0
    BODY = 1


TIGHTNESS = 50
DISTANCE_FACTOR = 1.2
PREVIOUS_INFLUENCE = 0.1


class CentipedeAI(MeleeAI):

    def __init__(self, entity: MeleeEnemy):
        super().__init__(entity)

    def _run_ai(self, world, delta_time: float):
        self.space_units(world, delta_time)
        self.run_head(world, delta_time)
        self.run_body(world, delta_time)
        self.entity.animate_generic()

    def run_head(self, world, delta_time: float):
        if self.entity.centipede_state is not CentipedeState.HEAD:
            return
        super()._run_ai(world, delta_time)

    def run_body(self, world, delta_time: float):
        if self.entity.centipede_state is not CentipedeState.BODY:
            return

        # Check if previous part exists
        if self.entity.previous_segment is None or self.entity.previous_segment.is_dead():
            self.entity.set_state(CentipedeState.HEAD)
            return

        # Accelerate towards previous segment
        me_to_segment = self.entity.previous_segment.center_position - self.entity.center_position

        distance = me_to_segment.magnitude()
        target_distance = self.entity.get_collision_radius() * DISTANCE_FACTOR
        direction = me_to_segment.normalize()

        acceleration = direction * TIGHTNESS
        acceleration += self.entity.previous_segment.velocity.normalize() * PREVIOUS_INFLUENCE
        acceleration *= (distance - self.entity.atlas.get_average_radius()) / target_distance * DISTANCE_FACTOR

        self.entity.accelerate_uncapped(acceleration)
