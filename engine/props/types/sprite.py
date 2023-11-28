import pygame

from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.graphics.textures.texture import Texture
from engine.graphics.textures.texture_animation import AnimationType
from engine.props.types.movable import Movable


class Sprite(Movable, pygame.sprite.Sprite):

    def __init__(self, animation_atlas: AnimationAtlas, position: Vector = Vector(), velocity: Vector = Vector(),
                 max_speed: float = 0, acceleration: float = 0):
        super().__init__(position, velocity, max_speed, acceleration)
        self.animation_atlas = animation_atlas.copy()
        self.current_animation = self.animation_atlas.texture_animations[0]
        self.sprite_width, self.sprite_height = self.current_animation.get_texture().image.get_size()
        self.base_width, self.base_height = self.sprite_width, self.sprite_height

    def get_texture(self) -> Texture:
        return self.current_animation.get_texture()

    def render(self, surface: pygame.Surface, screen_position: Vector) -> None:
        render_position = screen_position - Vector(*self.get_texture().image.get_size()) / 2
        surface.blit(self.current_animation.get_texture().image,
                     render_position.as_tuple())

    def get_center_position(self) -> Vector:
        return self.position + Vector(self.sprite_width // 2, self.sprite_height // 2)

    def play_animation(self, animation_type):
        if isinstance(animation_type, AnimationType):
            self.current_animation = self.animation_atlas.get_animation(animation_type)
        elif isinstance(animation_type, int):
            self.current_animation = self.animation_atlas.texture_animations[animation_type]
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
