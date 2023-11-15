from typing import List
from enum import Enum

import pygame

MOUSE_LEFT = 1
MOUSE_RIGHT = 3


class InputEnum(Enum):
    W = 0,
    A = 1,
    S = 2,
    D = 3,
    SPACE = 4,

    MOUSE_X = 5,
    MOUSE_Y = 6,
    LEFT_CLICK = 7,
    RIGHT_CLICK = 8


class InputManager:

    def __init__(self):
        pygame.init()
        self.w = 0
        self.a = 0
        self.s = 0
        self.d = 0

        self.space = 0
        self.left_click = 0
        self.right_click = 0
        self.mouse_x = 0
        self.mouse_y = 0

    def update(self, event: pygame.event) -> None:
        self._monitor(event)

    def read(self) -> List[int]:
        return [self.w, self.a, self.s, self.d, self.space, self.mouse_x, self.mouse_y, self.left_click,
                self.right_click]

    def _monitor(self, event: pygame.event) -> None:
        # Keyboard
        key_value = -1
        if event.type == pygame.KEYDOWN:
            key_value = 1
        elif event.type == pygame.KEYUP:
            key_value = 0

        if key_value != -1:
            if event.key == pygame.K_w:
                self.w = key_value
            elif event.key == pygame.K_a:
                self.a = key_value
            elif event.key == pygame.K_s:
                self.s = key_value
            elif event.key == pygame.K_d:
                self.d = key_value
            elif event.key == pygame.K_SPACE:
                self.space = key_value

        # Mouse
        mouse_value = -1
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_value = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_value = 0

        if mouse_value != -1:
            if event.button == MOUSE_LEFT:
                self.left_click = mouse_value
            elif event.button == MOUSE_RIGHT:
                self.right_click = mouse_value

        if event.type == pygame.MOUSEMOTION:
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
