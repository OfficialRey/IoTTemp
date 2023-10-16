from typing import Tuple, Union

import pygame

WHITE = (255, 255, 255)


class Widget:

    def __init__(self, area: Tuple[Union[float, int], Union[float, int], Union[float, int]]):
        self.area = pygame.Rect(area)

    def render(self, surface: pygame.Surface):
        raise NotImplementedError("Not implemented!")


class Label(Widget):

    def __init__(self, area: Tuple[Union[float, int], Union[float, int], Union[float, int]], text: str,
                 font_color: Tuple[int, int, int] = WHITE, background_color: Tuple[int, int, int] = None,
                 font: str = "comicsansms"):
        super().__init__(area)
        self.text_size = self.area.height
        self.text = text
        self.font = pygame.font.SysFont(font, self.text_size)
        self.font_color = font_color
        self.background_color = background_color
        self.render = self._load_render()

    def _load_render(self) -> pygame.Surface:
        return self.font.render(self.text, True, self.font_color)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.render, (self.area.x, self.area.y))
        if self.background_color is not None:
            surface.fill(self.background_color, self.area)


class Button(Widget):

    def __init__(self, area: Tuple[Union[float, int], Union[float, int], Union[float, int]]):
        super().__init__(area)

    def render(self, surface: pygame.Surface) -> None:
        pass
