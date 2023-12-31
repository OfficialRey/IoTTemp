import math
from typing import Union

import pygame

from engine.core.vector import Vector
from engine.graphics.animation.animation import AnimationType
from engine.graphics.animation.animation_manager import AnimationManager
from engine.graphics.atlas.atlas import Atlas
from engine.props.types.movable import Movable
from engine.util.constants import BLACK, WHITE, RED
from engine.world.collision import Collision, CollisionShape, CollisionInformation

GENERIC_ANIMATIONS = [AnimationType.WALKING_N, AnimationType.WALKING_NE, AnimationType.WALKING_E,
                      AnimationType.WALKING_SE, AnimationType.WALKING_S, AnimationType.WALKING_SW,
                      AnimationType.WALKING_W, AnimationType.WALKING_NW]

ANGLE_OFFSET = 360 / len(GENERIC_ANIMATIONS) * 0.5

HIT_BOX_FACTOR = 0.3


class Sprite(Movable, pygame.sprite.Sprite):

    def __init__(self, atlas: Atlas, max_speed: float = 0, acceleration: float = 0,
                 center_position: Vector = Vector(), velocity: Vector = Vector(),
                 animation_type: AnimationType = AnimationType.GENERIC):
        super().__init__(max_speed, acceleration, center_position, velocity,
                         Collision(center_position, (atlas.sprite_width + atlas.sprite_height) // 2,
                                   shape=CollisionShape.CIRCLE))
        self.atlas = atlas
        self.animation_manager = AnimationManager(self.atlas, animation_type)
        self.animation_manager.update_animation_type(AnimationType.GENERIC)

    def flash_image(self, flash_time: float):
        self.animation_manager.flash_image(flash_time)

    def get_surface(self) -> pygame.Surface:
        return self.animation_manager.get_surface()

    def render(self, surface: pygame.Surface, camera) -> None:
        surface.blit(self.get_surface(), self.get_render_position(camera).as_tuple())
        # self.draw_debug(surface, camera)

    def get_render_position(self, camera=None) -> Vector:
        if camera is not None:
            return camera.get_relative_position(self) - self.get_render_offset()
        return self.center_position - self.get_render_offset()

    def get_render_offset(self) -> Vector:
        return Vector(self.animation_manager.get_surface().get_width() // 2,
                      self.animation_manager.get_surface().get_height() // 2)

    def offset_animation(self):
        self.animation_manager.offset_animation()

    def update(self, world, delta_time: float) -> None:
        self.animation_manager.update(delta_time)
        super().update(world, delta_time)

    def set_rotation(self, rotation: float):
        self.animation_manager.set_rotation(rotation)

    def get_rotation(self):
        return self.animation_manager.get_rotation()

    def get_velocity_rotation(self):
        vector = Vector(self.velocity.x, -self.velocity.y).normalize()
        return math.degrees(math.atan2(*vector.as_tuple()))

    def animate_generic(self):
        index = min(int((self.get_velocity_rotation() + ANGLE_OFFSET) / 45), len(GENERIC_ANIMATIONS) - 1)
        self.animation_manager.update_animation_type(GENERIC_ANIMATIONS[index])

    def animate_rotation(self, target_position: Vector):
        position_to_target = target_position - self.center_position
        if position_to_target.x >= 0:
            self.animation_manager.update_animation_type(AnimationType.WALKING_E)
        else:
            self.animation_manager.update_animation_type(AnimationType.WALKING_W)

    def collide_generic(self, other) -> CollisionInformation:
        return self.collision.collides_with(other.collision)

    def get_collision_position(self):
        return self.center_position + Vector(self.animation_manager.get_surface().get_width(),
                                             self.animation_manager.get_surface().get_height())

    def get_collision_radius(self):
        return (
                self.animation_manager.get_surface().get_width() + self.animation_manager.get_surface().get_height()
        ) / 2 * HIT_BOX_FACTOR

    def play_animation(self, animation_type: Union[int, AnimationType]):
        if isinstance(animation_type, AnimationType):
            self.animation_manager.update_animation_type(animation_type)
        elif isinstance(animation_type, int):
            self.animation_manager.update_animation_index(animation_type)

    def draw_debug(self, surface: pygame.Surface, camera):
        pygame.draw.circle(surface, BLACK, (self.center_position - camera.get_position()).as_tuple(),
                           self.get_collision_radius() / 2)
        pygame.draw.circle(surface, WHITE, (self.center_position - camera.get_position()).as_tuple(), 3)
        pygame.draw.circle(surface, RED, self.get_render_position(camera).as_tuple(), 3)
