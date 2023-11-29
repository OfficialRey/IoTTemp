import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.enemy.data import UnitData
from engine.props.enemy.enemy import Enemy
from engine.props.enemy.storage.centipede.centipede_body import CentipedeBody
from engine.props.player.player import Player


class Centipede(Enemy):

    def __init__(self, texture_manager: TextureManager, position: Vector):
        super().__init__(texture_manager.centipede, UnitData.CENTIPEDE, position)
        self.position = Vector(100, 100)
        self.body_texture = texture_manager.centipede_body
        self.body = []

        self._create_body()

    def _create_body(self):
        length = 5

        self.body = []
        previous_segment = self
        for i in range(length):
            previous_segment = CentipedeBody(self.body_texture, previous_segment,
                                             previous_segment.get_center_position() - Vector.random().normalize() * self.sprite_width)
            self.body.append(previous_segment)

    def run_behaviour(self, world, delta_time: float):
        target = world.player

        self.accelerate((target.get_center_position() - self.get_center_position()).normalize())

        for body in self.body:
            body.update(world, delta_time)

        self.animate_generic()

    def render(self, surface: pygame.Surface, camera) -> None:
        super().render(surface, camera)
        for body in self.body:
            body.render(surface, camera)

    def on_hit(self):
        pass

    def on_death(self):
        pass

    def on_attack(self):
        pass

    def collides_with(self, other: pygame.sprite.Sprite):
        pass
