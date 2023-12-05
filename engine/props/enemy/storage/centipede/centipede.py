import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.bullet.bullet import Bullet
from engine.props.data import UnitData
from engine.props.enemy.enemy import Enemy
from engine.props.enemy.storage.centipede.centipede_body import CentipedeBody
from engine.props.enemy.storage.centipede.centipede_head import CentipedeHead
from engine.props.player.player import Player
from engine.props.types.collision import CollisionInformation
from engine.props.types.sprite import Sprite


class Centipede(Enemy):

    def __init__(self, texture_manager: TextureManager, center_position: Vector):
        super().__init__(texture_manager.centipede_head, UnitData.NONE, center_position)
        self.head_texture = texture_manager.centipede_head
        self.body_texture = texture_manager.centipede_body
        self.segments = []

        self._create_centipede()

    def _create_centipede(self):
        length = 50

        previous_segment = CentipedeHead(self, self.head_texture, self.center_position)
        self.segments = [previous_segment]
        for i in range(1, length):
            previous_segment = CentipedeBody(self, self.body_texture, previous_segment,
                                             previous_segment.center_position + Vector(-1,
                                                                                       0) * self.get_collision_radius())
            previous_segment.offset_animation()
            previous_segment.velocity = Vector()
            self.segments.append(previous_segment)

    def run_behaviour(self, world, delta_time: float):
        for segment in self.segments:
            segment.update(world, delta_time)

    def remove_dead_segments(self):
        to_remove = []
        for segment in self.segments:
            if segment.can_remove() or isinstance(segment, CentipedeBody) and segment.previous_segment is None:
                to_remove.append(segment)

        if len(to_remove) > 0:
            self.segments.remove(*to_remove)
            self.split_centipede()
            self.remove_dead_segments()

    def split_centipede(self):
        for i in range(len(self.segments) - 1):
            current_segment = self.segments[i]
            if isinstance(current_segment, CentipedeBody):
                # Create new head
                if not current_segment.has_head():
                    self.segments[i] = CentipedeHead(self, self.head_texture, current_segment.center_position)
                    self.segments[i + 1].previous_segment = self.segments[i]

    def render(self, surface: pygame.Surface, camera) -> None:
        segments = self.segments.copy()
        segments.reverse()
        for segment in segments:
            segment.render(surface, camera)

    def collide_generic(self, other) -> CollisionInformation:
        for segment in self.segments:
            collision_info = segment.collide_generic(other)
            if collision_info.hit:
                segment.on_collision(other, collision_info)
                return collision_info
        return CollisionInformation()

    def is_dead(self):
        return len(self.segments) == 0

    def on_hit(self):
        pass

    def on_death(self):
        pass

    def on_attack(self):
        pass

    def on_collision(self, other: Sprite, collision_info: CollisionInformation):
        if not isinstance(other, Bullet):
            return
        if not isinstance(other.owner, Player):
            return

        # The player shot me
        self.damage(other.bullet_type.get_attack(), collision_info)
        other.life_time = 0
