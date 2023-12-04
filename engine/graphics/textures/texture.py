from typing import Union

import pygame.image

from pygame.transform import scale

from engine.core.vector import Vector
from engine.util.constants import FULL_ROTATION
from engine.util.util import colorize_image

FLASH_COLOR_OFFSET = 150, 0, 0, 0


class Texture:

    def __init__(self, base_image: pygame.Surface, rotation_precision: int = 360):

        self.base_image = base_image.copy()
        self.rotation_precision = rotation_precision
        self.current_rotation = 0

        self.images = []
        self.flash_images = []

        self._initialise()

    def _initialise(self):
        self._load_images()
        self._colorize_flash_images()

    def _load_images(self):
        self.images = []
        self.flash_images = []

        for rotation in range(0, FULL_ROTATION, self.rotation_precision):
            image = pygame.transform.rotate(self.base_image.copy(), rotation)
            self.images.append(image)
            self.flash_images.append(image)

    def _colorize_flash_images(self):
        for i in range(len(self.flash_images)):
            self.flash_images[i] = colorize_image(self.flash_images[i], *FLASH_COLOR_OFFSET)

    def set_scale(self, image_scale: Union[Vector, float, int]):
        if image_scale == Vector(1, 1):
            return self.images
        if isinstance(image_scale, (float, int)):
            image_scale = Vector(image_scale, image_scale)

        for i in range(len(self.images)):
            image = self.images[i]
            flash_image = self.flash_images[i]
            self.images[i] = scale(image, (image.get_width() * image_scale.x, image.get_height() * image_scale.y))
            self.flash_images[i] = scale(flash_image,
                                         (flash_image.get_width() * image_scale.x,
                                          flash_image.get_height() * image_scale.y))

    def set_rotation(self, rotation: float):
        self.current_rotation = rotation

    def get_rotation(self):
        return self.current_rotation

    def mirror_texture(self, x_axis: bool = True, y_axis: bool = False):
        flip = x_axis, y_axis
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.flip(self.images[i], *flip)
            self.flash_images[i] = pygame.transform.flip(self.flash_images[i], *flip)

    def get_image(self):
        return self.images[int(self.current_rotation / self.rotation_precision)]

    def get_flash_image(self):
        return self.flash_images[int(self.current_rotation / self.rotation_precision)]

    def is_empty(self) -> bool:
        pixels = pygame.PixelArray(self.base_image)
        for x in range(self.base_image.get_width()):
            for y in range(self.base_image.get_height()):
                rgb = self.base_image.unmap_rgb(pixels[x][y])
                if rgb.a > 0:
                    return False
        del pixels
        return True
