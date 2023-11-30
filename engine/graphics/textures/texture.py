from typing import Union

import pygame.image

from engine.core.vector import Vector

MIN_COLOR = 0
MAX_COLOR = 255


class Texture:

    def __init__(self, base_image: pygame.Surface, image: pygame.Surface = None, scale: Vector = Vector(1, 1)):
        self.base_image = base_image
        self.image = image if image is not None else base_image.copy()
        self.scale = scale
        self.color_offsets = [0, 0, 0, 0]

    def reset(self):
        self.image = self.base_image.copy()
        self.colorize(*self.color_offsets)

    def set_scale(self, scale: Union[Vector, float, int]) -> pygame.Surface:
        if scale == Vector(1, 1):
            return self.image
        if isinstance(scale, (float, int)):
            scale = Vector(scale, scale)
        self.image = pygame.transform.scale(
            self.base_image,
            (self.base_image.get_width() * scale.x, self.base_image.get_height() * scale.y)
        )
        self.colorize(*self.color_offsets)
        return self.image

    def colorize(self, red_offset: int = 0, green_offset: int = 0, blue_offset: int = 0,
                 alpha_offset: int = 0) -> pygame.Surface:
        width, height = self.image.get_size()
        for x in range(width):
            for y in range(height):
                r, g, b, a = self.image.get_at((x, y))
                red = min(MAX_COLOR, max(MIN_COLOR, r + red_offset))
                green = min(MAX_COLOR, max(MIN_COLOR, g + green_offset))
                blue = min(MAX_COLOR, max(MIN_COLOR, b + blue_offset))
                alpha = min(MAX_COLOR, max(MIN_COLOR, a + alpha_offset))
                self.image.set_at((x, y), pygame.Color(red, green, blue, alpha))

        for i in range(len(self.color_offsets)):
            self.color_offsets[i] += (red_offset, green_offset, blue_offset, alpha_offset)[i]

        return self.image

    def mirror(self, x_axis: bool = True, y_axis: bool = False):
        width = self.image.get_width()
        height = self.image.get_height()

        new_pixels = [[pygame.Color(0, 0, 0) for _ in range(height)] for _ in range(width)]
        pixels = pygame.PixelArray(self.image)
        for x in range(width):
            for y in range(height):
                # Mirror image
                color = pygame.Color(self.image.unmap_rgb(pixels[x][y]))
                x_pos = x
                y_pos = y
                if x_axis:
                    x_pos = width - x - 1
                if y_axis:
                    y_pos = height - y - 1
                new_pixels[x_pos][y_pos] = color

        for x in range(width):
            for y in range(height):
                pixels[x][y] = new_pixels[x][y]
        del pixels
        return self.image

    def copy(self):
        return Texture(self.base_image, self.image)

    def is_empty(self) -> bool:
        pixels = pygame.PixelArray(self.image)
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                rgb = self.image.unmap_rgb(pixels[x][y])
                if rgb.a > 0:
                    return False
        del pixels
        return True
