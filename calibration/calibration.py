from typing import Tuple

import pygame.image

from engine.core.vector import Vector
from engine.core.window import Window
from engine.graphics.textures.texture_manager import TextureManager
from engine.util.constants import YELLOW


class Calibration:

    def __init__(self, window: Window, texture_manager: TextureManager):
        self.calibrator = texture_manager.calibrator
        self.calculation_parameters = []
        self.window = window
        window_size = self.window.get_size()
        self.calibration_points = [
            window_size * 0.2,
            Vector(window_size.x * 0.8, window_size.y * 0.2),
            Vector(window_size.x * 0.2, window_size.y * 0.8),
            window_size * 0.8,
            window_size * 0.5
        ]
        self.current_index = 0

    def run(self, window: Window):
        self._render(window)

    def _render(self, window: Window):
        window.fill(YELLOW)
        window.surface.blit(self.calibrator.get_texture(0).image, self.calibration_points[self.current_index])
        pygame.display.flip()

    def get_calibration(self, pitch: float, yaw: float) -> Tuple[int, int]:
        """
        Calculates the actual cursor x and y positions using pitch and yaw
        """
        pass
