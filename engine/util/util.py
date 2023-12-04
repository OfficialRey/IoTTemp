import pygame

from engine.util.constants import MIN_COLOR, MAX_COLOR


def show_cursor(visibility: bool = True) -> None:
    pygame.mouse.set_visible(visibility)


def colorize_image(surface: pygame.Surface, red_offset: int = 0, green_offset: int = 0, blue_offset: int = 0,
                   alpha_offset: int = 0):
    width, height = surface.get_size()
    for x in range(width):
        for y in range(height):
            r, g, b, a = surface.get_at((x, y))
            red = min(MAX_COLOR, max(MIN_COLOR, r + red_offset))
            green = min(MAX_COLOR, max(MIN_COLOR, g + green_offset))
            blue = min(MAX_COLOR, max(MIN_COLOR, b + blue_offset))
            alpha = min(MAX_COLOR, max(MIN_COLOR, a + alpha_offset))
            surface.set_at((x, y), pygame.Color(red, green, blue, alpha))
    return surface
