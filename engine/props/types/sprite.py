import math
from typing import Union

import pygame

from engine.core.vector import Vector
from engine.graphics.animation.animation import AnimationType
from engine.graphics.animation.animation_manager import AnimationManager
from engine.graphics.atlas.animation import AnimationAtlas
from engine.graphics.atlas.atlas import Atlas
from engine.props.types.movable import Movable

GENERIC_ANIMATIONS = [AnimationType.WALKING_N, AnimationType.WALKING_NE, AnimationType.WALKING_E,
                      AnimationType.WALKING_SE, AnimationType.WALKING_S, AnimationType.WALKING_SW,
                      AnimationType.WALKING_W, AnimationType.WALKING_NW]

ANGLE_OFFSET = 360 / len(GENERIC_ANIMATIONS) * 0.5

HIT_BOX_FACTOR = 0.75


class Sprite(Movable, pygame.sprite.Sprite):

    def __init__(self, atlas: Atlas, max_speed: float = 0, acceleration: float = 0,
                 position: Vector = Vector(), velocity: Vector = Vector(),
                 animation_type: AnimationType = AnimationType.GENERIC):
        super().__init__(max_speed, acceleration, position, velocity)
        self.atlas = atlas
        self.animation_manager = AnimationManager(self.atlas, animation_type)
        self.sprite_width, self.sprite_height = self.atlas.sprite_width, self.atlas.sprite_height
        self.base_width, self.base_height = self.sprite_width, self.sprite_height

    def flash_image(self, flash_time: float):
        self.animation_manager.flash_image(flash_time)

    def get_surface(self) -> pygame.Surface:
        return self.animation_manager.get_surface(self.atlas)

    def render(self, surface: pygame.Surface, camera) -> None:
        render_position = camera.get_relative_position(self) - Vector(*self.get_surface().get_size()) / 2
        surface.blit(self.get_surface(), render_position.as_tuple())

    def get_center_position(self) -> Vector:
        return self.position + Vector(self.sprite_width // 2, self.sprite_height // 2)

    def offset_animation(self):
        self.animation_manager.offset_animation()

    def update(self, world, delta_time: float) -> None:
        self.animation_manager.update(delta_time)
        super().update(world, delta_time)

    def set_scale(self, scale: Vector):
        self.atlas.set_scale(scale)

    def set_size(self, width: int, height: int):
        x_scale = width / self.base_width
        y_scale = height / self.base_height
        self.set_scale(Vector(x_scale, y_scale))

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

    def collide_generic(self, other) -> bool:
        distance = self.get_center_position().distance(other.get_center_position())
        collision_radius = max(self.get_collision_radius(), other.get_collision_radius())
        return distance <= collision_radius

    def get_collision_radius(self):
        return (self.sprite_width + self.sprite_height) / 2 * HIT_BOX_FACTOR

    def play_animation(self, animation_type: Union[int, AnimationType]):
        if isinstance(animation_type, AnimationType):
            self.animation_manager.update_animation_type(animation_type)
        elif isinstance(animation_type, int):
            self.animation_manager.update_animation_index(animation_type)
