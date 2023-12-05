from engine.core.vector import Vector
from engine.graphics.atlas.animation import AnimationAtlas
from engine.props.bullet.bullet import Bullet
from engine.props.data import UnitData
from engine.props.enemy.enemy import MeleeEnemy
from engine.props.enemy.storage.centipede.centipede_head import CentipedeHead
from engine.props.player.player import Player
from engine.props.types.collision import CollisionInformation
from engine.props.types.sprite import Sprite

TIGHTNESS = 50
DISTANCE_FACTOR = 1.2
PREVIOUS_INFLUENCE = 0.1


class CentipedeBody(MeleeEnemy):

    def __init__(self, core, atlas: AnimationAtlas, previous_segment: MeleeEnemy, center_position: Vector):
        super().__init__(atlas, UnitData.CENTIPEDE_BODY, center_position)
        self.core = core
        self.previous_segment = previous_segment

    def run_behaviour(self, world, delta_time: float):
        # Accelerate towards previous segment
        me_to_segment = self.previous_segment.center_position - self.center_position

        distance = me_to_segment.magnitude()
        target_distance = self.get_collision_radius() * DISTANCE_FACTOR
        direction = me_to_segment.normalize()

        acceleration = direction * TIGHTNESS
        acceleration += self.previous_segment.velocity.normalize() * PREVIOUS_INFLUENCE
        acceleration *= (distance - self.atlas.get_average_radius()) / target_distance * DISTANCE_FACTOR

        self.accelerate(acceleration, delta_time)
        self.animate_generic()

    def on_hit(self):
        pass

    def on_death(self):
        self.core.remove_dead_segments()

    def on_attack(self):
        pass

    def on_collision(self, other: Sprite, collision_info: CollisionInformation):
        if not isinstance(other, Bullet):
            return
        if not isinstance(other.owner, Player):
            return

        # The player shot me
        self.damage(other.get_attack(), collision_info)
        other.life_time = 0

    def has_head(self):
        """
        Trace back segment chain to check if this centipede has a head
        """

        # Cannot have a head if segment chain ends here
        if self.is_dead() or self.previous_segment.is_dead():
            return False

        # Previous segment is the head
        if isinstance(self.previous_segment, CentipedeHead):
            return True

        # Look further
        if isinstance(self.previous_segment, CentipedeBody):
            return self.previous_segment.has_head()

        # Unknown state
        return False
