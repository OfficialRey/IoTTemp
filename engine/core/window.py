from typing import Tuple

import pygame

from engine.core.vector import Vector
from engine.util.constants import BLACK


class Window:
    surface: pygame.Surface
    window_flags: int
    full_screen: bool

    def __init__(self, resolution: Vector, full_screen: bool = False):
        pygame.display.init()
        self.resolution = resolution
        self.change_dimensions(resolution, full_screen)

    def update(self, event: pygame.event) -> None:
        if event.type == pygame.QUIT:
            exit(0)

    def change_dimensions(self, resolution: Vector = None, full_screen: bool = False) -> None:
        if resolution is not None:
            self.resolution = resolution
        self.full_screen = full_screen
        self.window_flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | int(full_screen) * pygame.FULLSCREEN
        self.surface = pygame.display.set_mode((self.resolution.as_tuple()), self.window_flags)

    def fill(self, color: Tuple[int, int, int] = BLACK) -> None:
        self.surface.fill(color, (0, 0, *self.resolution.as_tuple()))

    def get_width(self):
        return self.surface.get_width()

    def get_height(self):
        return self.surface.get_height()

    def get_size(self) -> Vector:
        return Vector(*self.surface.get_size())
