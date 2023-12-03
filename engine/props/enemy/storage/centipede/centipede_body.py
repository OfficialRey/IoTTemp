from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.bullet.bullet import Bullet
from engine.props.data import UnitData
from engine.props.enemy.enemy import Enemy
from engine.props.enemy.storage.centipede.centipede_head import CentipedeHead
from engine.props.player.player import Player
from engine.props.types.sprite import Sprite

TIGHTNESS = 100
DISTANCE_FACTOR = 4


class CentipedeBody(Enemy):

    def __init__(self, animation_atlas: AnimationAtlas, previous_segment: Enemy, position: Vector):
        super().__init__(animation_atlas, UnitData.CENTIPEDE_BODY, position)
        self.position = position
        self.previous_segment = previous_segment

    def run_behaviour(self, world, delta_time: float):
        # Accelerate towards previous segment
        me_to_segment = self.previous_segment.position - self.position

        distance = me_to_segment.magnitude()
        target_distance = self.sprite_width * DISTANCE_FACTOR
        direction = me_to_segment.normalize()
        acceleration = (direction.inverse() + direction * distance / target_distance) * TIGHTNESS

        self.accelerate(acceleration, delta_time)
        self.animate_generic()

    def on_hit(self):
        pass

    def on_death(self):
        pass

    def on_attack(self):
        pass

    def on_collision(self, other: Sprite):
        if not isinstance(other, Bullet):
            return
        if not isinstance(other.owner, Player):
            return

        # The player shot me
        self.damage(other.get_attack())
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
