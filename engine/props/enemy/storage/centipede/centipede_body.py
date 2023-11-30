import pygame

from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.enemy.data import UnitData
from engine.props.enemy.enemy import Enemy
from engine.props.player.player import Player

TIGHTNESS = 100
DISTANCE_FACTOR = 0.75


class CentipedeBody(Enemy):

    def __init__(self, animation_atlas: AnimationAtlas, previous_segment: Enemy, position: Vector):
        super().__init__(animation_atlas, UnitData.CENTIPEDE_BODY, position)
        self.position = position
        self.previous_segment = previous_segment

    def run_behaviour(self, delta_time: float, target: Player):
        # Accelerate towards previous segment
        me_to_segment = self.previous_segment.position - self.position

        distance = me_to_segment.magnitude()
        target_distance = self.sprite_width * DISTANCE_FACTOR
        direction = me_to_segment.normalize()
        acceleration = (direction.inverse() + direction * distance / target_distance) * TIGHTNESS

        self.accelerate(acceleration)
        self.animate_generic()

    def on_hit(self):
        pass

    def on_death(self):
        pass

    def on_attack(self):
        pass

    def collides_with(self, other: pygame.sprite.Sprite):
        pass
