import pygame

from engine.graphics.textures.texture import Texture


def get_texture(source: pygame.Surface, sprite_width: int, sprite_height: int, x: int, y: int):
    return Texture(source.subsurface((x, y, sprite_width, sprite_height)))
