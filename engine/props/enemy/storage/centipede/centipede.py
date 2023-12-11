import pygame

from random import random

from engine.core.vector import Vector
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.data import UnitData
from engine.props.enemy.ai.centipede_ai import CentipedeAI
from engine.props.enemy.enemy import MeleeEnemy
from engine.props.enemy.storage.centipede.centipede_body import CentipedeBody
from engine.props.enemy.storage.centipede.centipede_head import CentipedeHead
from engine.sound.game_sound import SoundEngine
from engine.world.collision import CollisionInformation


class Centipede(MeleeEnemy):

    def __init__(self, sound_engine: SoundEngine, texture_manager: TextureManager, center_position: Vector, level: int):
        super().__init__(sound_engine, texture_manager.centipede_head, UnitData.NONE, center_position)
        self.head_texture = texture_manager.centipede_head
        self.body_texture = texture_manager.centipede_body
        self.segments = []
        self.length = int(level / 5 + 3 + random() * 3)

        self.ai = CentipedeAI(self)

        self._create_centipede()

    def _create_centipede(self):
        previous_segment = CentipedeHead(self.sound_engine, self, self.head_texture, self.center_position)
        self.segments = [previous_segment]
        for i in range(1, self.length):
            new_position = previous_segment.center_position + Vector(-1, 0) * self.get_collision_radius()
            previous_segment = CentipedeBody(self.sound_engine, self, self.body_texture, previous_segment, new_position)

            previous_segment.offset_animation()
            previous_segment.velocity = Vector()
            self.segments.append(previous_segment)

    def run_behaviour(self, world, delta_time: float):
        # Fix Position of entity
        self.center_position = self.segments[0].center_position
        self.ai.run(world, delta_time)

    def render(self, surface: pygame.Surface, camera) -> None:
        segments = self.segments.copy()
        segments.reverse()
        for segment in segments:
            segment.render(surface, camera)

    def collide_generic(self, other) -> CollisionInformation:
        for segment in self.segments:
            collision_info = segment.collide_generic(other)
            if collision_info.hit:
                segment.on_generic_collision(other, collision_info)
                return CollisionInformation()
        return CollisionInformation()

    def is_dead(self):
        return len(self.segments) == 0

    def on_hit(self):
        pass

    def on_attack(self):
        pass
