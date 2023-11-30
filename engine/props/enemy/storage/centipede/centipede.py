from typing import List

import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.bullet.bullet import Bullet
from engine.props.data import UnitData
from engine.props.enemy.enemy import Enemy
from engine.props.enemy.storage.centipede.centipede_body import CentipedeBody
from engine.props.enemy.storage.centipede.centipede_head import CentipedeHead
from engine.props.player.player import Player
from engine.props.types.sprite import Sprite


class Centipede(Enemy):

    def __init__(self, texture_manager: TextureManager, position: Vector):
        super().__init__(texture_manager.centipede_head, UnitData.NONE, position)
        self.head_texture = texture_manager.centipede_head
        self.body_texture = texture_manager.centipede_body
        self.segments = []

        self._create_centipede()

    def run_behaviour(self, world, delta_time: float):
        for segment in self.segments:
            segment.update(world, delta_time)
        self.remove_dead_segments()

    def remove_dead_segments(self):
        to_remove = []
        for segment in self.segments:
            if segment.is_dead():
                to_remove.append(segment)

        if len(to_remove) > 0:
            self.segments.remove(*to_remove)
            self.split_centipede()

    def split_centipede(self):
        has_head = False
        for i in range(len(self.segments) - 1):

            # Remember if the chained segments have a head
            if isinstance(self.segments[i], CentipedeHead):
                has_head = True

            # Case 1: Head got removed
            if isinstance(self.segments[i], CentipedeBody) and not has_head:
                self.segments[i] = CentipedeHead(self.head_texture, self.segments[i].position)
                self.segments[i + 1].previous_segment = self.segments[i]
                has_head = True
                continue

            # Case 2: Center part is destroyed
            if isinstance(self.segments[i], CentipedeBody) and isinstance(self.segments[i + 1], CentipedeBody):
                if self.segments[i + 1].previous_segment != self.segments[i]:
                    self.segments[i] = CentipedeHead(self.head_texture, self.segments[i].position)
                    self.segments[i + 1].previous_segment = self.segments[i]

    def _create_centipede(self):
        length = 20

        previous_segment = CentipedeHead(self.head_texture, self.position)
        self.segments = [previous_segment]
        for i in range(length):
            previous_segment = CentipedeBody(self.body_texture, previous_segment, previous_segment.position)
            previous_segment.offset_animation()
            self.segments.append(previous_segment)

    def render(self, surface: pygame.Surface, camera) -> None:
        segments = self.segments.copy()
        segments.reverse()
        for segment in segments:
            segment.render(surface, camera)

    def collide_generic(self, other) -> bool:
        for segment in self.segments:
            if segment.collide_generic(other):
                segment.on_collision(other)
                return False

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

    def set_scale(self, scale: Vector):
        super().set_scale(scale)
        for segment in self.segments:
            segment.set_scale(scale)
