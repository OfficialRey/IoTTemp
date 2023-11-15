import pygame

from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.graphics.textures.texture_animation import AnimationType
from engine.graphics.textures.texture import Texture
from engine.util.constants import VECTOR_UP


class Movable:

    def __init__(self, position: Vector = Vector(), velocity: Vector = Vector(), max_speed: float = 0):
        super().__init__()
        self.position = position
        self.velocity = velocity
        self.max_speed = max_speed

    def accelerate(self, acceleration: Vector) -> None:
        self.velocity += acceleration
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    def update(self, delta_time: float) -> None:
        self.position += self.velocity * delta_time


class Sprite(Movable, pygame.sprite.Sprite):

    def __init__(self, animation_atlas: AnimationAtlas, position: Vector = Vector(), velocity: Vector = Vector(),
                 max_speed: float = 0):
        super().__init__(position, velocity, max_speed)
        self.animation_atlas = animation_atlas
        self.current_animation = self.animation_atlas.texture_animations[0]
        self.sprite_width, self.sprite_height = self.current_animation.get_texture().image.get_size()
        self.base_width, self.base_height = self.sprite_width, self.sprite_height
        self.relative_position = self.position

    def get_texture(self) -> Texture:
        return self.current_animation.get_texture()

    def render(self, surface: pygame.Surface, screen_position: Vector) -> None:
        surface.blit(self.current_animation.get_texture().image,
                     screen_position.as_tuple())

    def get_center_position(self) -> Vector:
        return self.position + Vector(self.sprite_width // 2, self.sprite_height // 2)

    def collides_with(self, other) -> bool:
        return self.get_center_position().distance(other.get_center_position()) <= \
               (min(self.sprite_width, self.sprite_height) + min(other.sprite_width, other.sprite_height)) / 2

    def play_animation(self, animation_type: AnimationType):
        self.current_animation = self.animation_atlas.get_animation(animation_type)
        self.current_animation.reset()

    def update(self, delta_time: float) -> None:
        self.current_animation.update(delta_time)
        super().update(delta_time)

    def set_scale(self, scale: Vector):
        self.animation_atlas.set_scale(scale)

    def set_size(self, width: int, height: int):
        x_scale = width / self.base_width
        y_scale = height / self.base_height
        self.set_scale(Vector(x_scale, y_scale))

    def update_relative_position(self, camera):
        self.relative_position = camera.get_relative_position(self)


class Entity(Sprite):

    def __init__(self, animation_atlas: AnimationAtlas, max_health: int, attack: int, defense: int, max_speed: float,
                 position: Vector = Vector(), velocity: Vector = Vector()):
        super().__init__(animation_atlas, position, velocity, max_speed)
        self.max_health = max_health
        self.health = self.max_health
        self.attack = attack
        self.defense = defense

    def _act(self, delta_time: float) -> None:
        raise NotImplementedError("Implement a behaviour for this props!")

    def update(self, delta_time: float):
        # Animation update
        angle = VECTOR_UP.angle(self.velocity)
        self._act(delta_time)
        super().update(delta_time)
