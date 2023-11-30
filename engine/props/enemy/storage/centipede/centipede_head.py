import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.bullet.bullet import Bullet
from engine.props.enemy.data import UnitData
from engine.props.enemy.enemy import Enemy
from engine.props.enemy.storage.centipede.centipede_body import CentipedeBody
from engine.props.player.player import Player
from engine.props.types.sprite import Sprite


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
            previous_segment.offset_animation()
            self.body.append(previous_segment)

    def run_behaviour(self, world, delta_time: float):
        target = world.player

        self.accelerate((target.get_center_position() - self.get_center_position()).normalize())

        for body in self.body:
            body.update(world, delta_time)

        self.animate_generic()

    def render(self, surface: pygame.Surface, camera) -> None:
        bodies = self.body.copy()
        bodies.reverse()
        for body in bodies:
            body.render(surface, camera)
        super().render(surface, camera)

    def collide_generic(self, other) -> bool:
        for body in self.body:
            if body.collide_generic(other):
                body.on_collision(other)
                return False
        return super().collide_generic(other)

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
        self.damage(other.bullet_type.get_damage())
        other.life_time = 0
