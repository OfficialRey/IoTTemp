import pygame

from engine.core.input_manager import InputManager
from engine.core.vector import Vector
from engine.graphics.textures.texture_animation import AnimationType
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.entity import Entity
from engine.props.player.cursor import Cursor


class Player(Entity):

    def __init__(self, texture_manager: TextureManager):
        super().__init__(texture_manager.player, 100, 20, 20, 10)
        self.input_manager = None
        self.cursor = Cursor(texture_manager)
        self.cursor.play_animation(AnimationType.GENERIC)

    def _act(self, delta_time: float) -> None:
        self.cursor.update(delta_time)

    # Format: [w, a, s, d, space, mouse_x, mouse_y, left_click, right_click]

    def handle_input(self, input_manager: InputManager):
        position = Vector(input_manager.mouse_x, input_manager.mouse_y)
        self.cursor.set_position(position)

    def render(self, surface: pygame.Surface, screen_position: Vector) -> None:
        self.cursor.render(surface, self.cursor.position)
        super(Player, self).render(surface, screen_position)
