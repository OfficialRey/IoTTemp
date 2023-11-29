import pygame

from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.enemy.data import UnitData
from engine.props.enemy.enemy import Enemy


class CentipedeBody(Enemy):

    def __init__(self, animation_atlas: AnimationAtlas, previous_segment: Enemy, position: Vector):
        super().__init__(animation_atlas, UnitData.CENTIPEDE_BODY)
        self.position = position
        self.previous_segment = previous_segment

    def run_behaviour(self, delta_time: float):
        # Accelerate towards previous segment
        me_to_segment = self.previous_segment.position - self.position
        acceleration = me_to_segment.normalize()
        if me_to_segment.magnitude() < self.sprite_width:
            acceleration *= 0.5
        self.accelerate(acceleration)

    def on_hit(self):
        pass

    def on_death(self):
        pass

    def on_attack(self):
        pass

    def collides_with(self, other: pygame.sprite.Sprite):
        pass
