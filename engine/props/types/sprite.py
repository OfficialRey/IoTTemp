import math
import random

import pygame

from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.graphics.textures.texture import Texture
from engine.graphics.textures.texture_animation import AnimationType
from engine.props.types.movable import Movable

GENERIC_ANIMATIONS = [AnimationType.WALKING_N, AnimationType.WALKING_NE, AnimationType.WALKING_E,
                      AnimationType.WALKING_SE, AnimationType.WALKING_S, AnimationType.WALKING_SW,
                      AnimationType.WALKING_W, AnimationType.WALKING_NW]

ANGLE_OFFSET = 360 / len(GENERIC_ANIMATIONS) * 0.5

HIT_BOX_FACTOR = 0.5


class Sprite(Movable, pygame.sprite.Sprite):

    def __init__(self, animation_atlas: AnimationAtlas, max_speed: float = 0, acceleration: float = 0,
                 position: Vector = Vector(), velocity: Vector = Vector()):
        super().__init__(max_speed, acceleration, position, velocity)
        self.animation_atlas = animation_atlas.copy()
        self.current_animation = self.animation_atlas.texture_animations[0]
        self.sprite_width, self.sprite_height = self.current_animation.get_texture().image.get_size()
        self.base_width, self.base_height = self.sprite_width, self.sprite_height
        self.flash_time = 0

    def flash(self, time: float):
        self.flash_time = time

    def get_texture(self) -> Texture:
        if self.flash_time > 0:
            return self.current_animation.get_flash_texture()
        return self.current_animation.get_texture()

    def render(self, surface: pygame.Surface, camera) -> None:
        render_position = camera.get_relative_position(self) - Vector(*self.get_texture().image.get_size()) / 2
        surface.blit(self.current_animation.get_texture().image,
                     render_position.as_tuple())

    def get_center_position(self) -> Vector:
        return self.position + Vector(self.sprite_width // 2, self.sprite_height // 2)

    def offset_animation(self):
        self.current_animation.offset_animation(self.current_animation.target_time * random.random())

    def play_animation(self, animation_type):
        if self.current_animation.animation_type == animation_type:
            return
        if isinstance(animation_type, AnimationType):
            self.current_animation = self.animation_atlas.get_animation(animation_type)
        elif isinstance(animation_type, int):
            self.current_animation = self.animation_atlas.texture_animations[animation_type]
        self.current_animation.reset()

    def update(self, world, delta_time: float) -> None:
        self.current_animation.update(delta_time)
        self.flash_time -= delta_time
        super().update(world, delta_time)

    def set_scale(self, scale: Vector):
        self.animation_atlas.set_scale(scale)

    def set_size(self, width: int, height: int):
        x_scale = width / self.base_width
        y_scale = height / self.base_height
        self.set_scale(Vector(x_scale, y_scale))

    # TODO: Fix animation system
    def animate_generic(self):
        vector = Vector(self.velocity.x, -self.velocity.y)
        angle = math.degrees(math.atan2(*vector.as_tuple()))
        index = min(int((angle + ANGLE_OFFSET) / 45), len(GENERIC_ANIMATIONS) - 1)
        self.play_animation(GENERIC_ANIMATIONS[index])

    def collide_generic(self, other) -> bool:
        distance = self.get_center_position().distance(other.get_center_position())
        collision_radius = max(self.get_collision_radius(), other.get_collision_radius())
        return distance <= collision_radius

    def get_collision_radius(self):
        return (self.sprite_width + self.sprite_height) / 2 * HIT_BOX_FACTOR
