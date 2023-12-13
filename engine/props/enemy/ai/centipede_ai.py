from enum import IntEnum

from engine.props.enemy.ai.ai import MeleeAI
from engine.props.enemy.enemy import MeleeEnemy


class CentipedeState(IntEnum):
    HEAD = 0
    BODY = 1


DISTANCE_FACTOR = 1
PREVIOUS_INFLUENCE = 0.3
BODY_ACCELERATION_FACTOR = 100
MAX_BODY_ACCELERATION_STRENGTH = 100


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

        previous = self.entity.previous_segment

        # Calculate target position
        target_distance = self.entity.atlas.get_average_radius() * DISTANCE_FACTOR
        target_position = previous.center_position - previous.velocity.normalize() * target_distance
        target_direction = (target_position - self.entity.center_position).normalize()

        # Calculate influence of previous segment
        previous_velocity = previous.velocity.normalize()

        # Calculate final acceleration
        acceleration = target_direction * (1 - PREVIOUS_INFLUENCE) + previous_velocity * PREVIOUS_INFLUENCE

        # Apply acceleration
        self.entity.accelerate_normalized(acceleration, delta_time)
