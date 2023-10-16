import pygame

from engine.graphics.textures.texture import Texture
from engine.util.constants import TRANSPARENCY


def get_texture(source: pygame.Surface, sprite_width: int, sprite_height: int, x: int, y: int):
    image = pygame.Surface((sprite_width, sprite_height))
    image.blit(source, (0, 0), (x, y, sprite_width, sprite_height))
    image.set_colorkey(TRANSPARENCY)
    return Texture(image)
