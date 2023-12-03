from typing import Union, List

import pygame.image

from engine.core.vector import Vector

MIN_COLOR = 0
MAX_COLOR = 255


class Texture:

    def __init__(self, base_image: pygame.Surface, image: pygame.Surface = None, flash_image: pygame.Surface = None,
                 scale: Vector = Vector(1, 1), mirror: List[bool] = None, flash_color_offset: List[int] = None,
                 has_flash_image: bool = False):
        if mirror is None:
            mirror = [False, False]
        if flash_color_offset is None:
            flash_color_offset = [150, 0, 0, 0]
        self.base_image = base_image
        self.image = image if image is not None else base_image.copy()
        self.flash_image = flash_image
        self.has_flash_image = has_flash_image
        self.scale = scale
        self.flash_color_offset = flash_color_offset
        self.mirror = mirror
        if flash_image is None:
            self.flash_image = self.image.copy()
            self.colorize_flash_image(*self.flash_color_offset)

    def reset(self):
        self.image = self.base_image.copy()
        self.flash_image = self.base_image.copy()
        self.colorize_flash_image(*self.flash_color_offset)

    def set_scale(self, scale: Union[Vector, float, int]) -> pygame.Surface:
        if scale == Vector(1, 1):
            return self.image
        if isinstance(scale, (float, int)):
            scale = Vector(scale, scale)
        self.image = pygame.transform.scale(
            self.base_image,
            (self.base_image.get_width() * scale.x, self.base_image.get_height() * scale.y)
        )
        self.flash_image = self.image.copy()
        self.colorize_flash_image(*self.flash_color_offset)
        return self.image

    # TODO: Improve performance
    def colorize_flash_image(self, red_offset: int = 0, green_offset: int = 0, blue_offset: int = 0,
                             alpha_offset: int = 0) -> pygame.Surface:
        if not self.has_flash_image:
            return self.flash_image
        width, height = self.flash_image.get_size()
        for x in range(width):
            for y in range(height):
                r, g, b, a = self.flash_image.get_at((x, y))
                red = min(MAX_COLOR, max(MIN_COLOR, r + red_offset))
                green = min(MAX_COLOR, max(MIN_COLOR, g + green_offset))
                blue = min(MAX_COLOR, max(MIN_COLOR, b + blue_offset))
                alpha = min(MAX_COLOR, max(MIN_COLOR, a + alpha_offset))
                self.flash_image.set_at((x, y), pygame.Color(red, green, blue, alpha))
        return self.flash_image

    def mirror_texture(self, x_axis: bool = True, y_axis: bool = False):
        self.mirror = [x_axis, y_axis]
        self.image = pygame.transform.flip(self.image, x_axis, y_axis)
        self.flash_image = pygame.transform.flip(self.flash_image, x_axis, y_axis)
        return self.image

    def copy(self):
        return Texture(self.base_image.copy(), self.image.copy(), self.flash_image.copy(), self.scale, self.mirror,
                       self.flash_color_offset, self.has_flash_image)

    def is_empty(self) -> bool:
        pixels = pygame.PixelArray(self.image)
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                rgb = self.image.unmap_rgb(pixels[x][y])
                if rgb.a > 0:
                    return False
        del pixels
        return True
