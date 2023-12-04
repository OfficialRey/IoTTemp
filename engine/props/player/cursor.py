import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.types.sprite import Sprite


class Cursor(Sprite):

    def __init__(self, texture_manager: TextureManager):
        super().__init__(texture_manager.cursor)
        self.position = Vector()

    def set_position(self, position: Vector):
        self.position = position

    def render(self, surface: pygame.Surface, camera) -> None:
        surface.blit(self.get_surface(), self.position.as_tuple())
