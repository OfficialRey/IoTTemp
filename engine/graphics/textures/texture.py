from typing import Union

import pygame.image

from engine.core.vector import Vector


class Texture:

    def __init__(self, base_image: pygame.Surface, image: pygame.Surface = None, scale: Vector = Vector(1, 1)):
        self.base_image = base_image
        self.image = image if image is not None else base_image.copy()
        self.scale = scale
        print(self.is_empty())

    def reset(self):
        self.image = self.base_image.copy()

    def set_scale(self, scale: Vector) -> pygame.Surface:
        self.image = pygame.transform.scale(
            self.base_image,
            (self.base_image.get_width() * scale.x, self.base_image.get_height() * scale.y)
        )
        return self.image

    def colorize(self, hue: int = None) -> pygame.Surface:
        if hue is not None:
            pixels = pygame.PixelArray(self.image)
            for x in range(self.image.get_width()):
                for y in range(self.image.get_height()):
                    rgb = self.image.unmap_rgb(pixels[x][y])
                    color = pygame.Color(*rgb)
                    h, s, l, a = color.hsla
                    color.hsla = (int(hue)) % 360, int(s), int(l), int(a)
                    pixels[x][y] = color
            del pixels
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
