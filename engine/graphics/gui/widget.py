from typing import Tuple, Union

import pygame

WHITE = (255, 255, 255)


class Widget:

    def __init__(self, area: Tuple[Union[float, int], Union[float, int], Union[float, int], Union[float, int]]):
        self.area = pygame.Rect(area)
        self.enabled = True

    def set_area(self, area: Tuple[Union[float, int], Union[float, int], Union[float, int], Union[float, int]]):
        self.area = pygame.Rect(area)

    def render(self, surface: pygame.Surface):
        raise NotImplementedError("Not implemented!")


class Label(Widget):

    def __init__(self, area: Tuple[Union[float, int], Union[float, int], Union[float, int], Union[float, int]],
                 text: str = None,
                 font_color: Tuple[int, int, int] = WHITE, background_color: Tuple[int, int, int] = None,
                 font: str = "comicsansms"):
        super().__init__(area)
        self.text_size = self.area.height
        self.text = text
        self.font = pygame.font.SysFont(font, self.text_size)
        self.font_color = font_color
        self.background_color = background_color
        self.base_render_content = None
        self.render_content = None
        if self.text is not None:
            self.render_content = self._load_render()

    def _load_render(self) -> pygame.Surface:
        return self.font.render(self.text, True, self.font_color)

    def set_content(self, image: pygame.Surface):
        if image is not None:
            self.base_render_content = image.copy()
            self.render_content = pygame.transform.scale(self.base_render_content, (self.area.width, self.area.height))

    def update_content(self):
        self.set_content(self.base_render_content)

    def set_area(self, area: Tuple[Union[float, int], Union[float, int], Union[float, int], Union[float, int]]):
        super().set_area(area)
        self.update_content()

    def render(self, surface: pygame.Surface) -> None:
        if self.background_color is not None:
            surface.fill(self.background_color, self.area)
        if self.render_content is not None:
            surface.blit(self.render_content, (self.area.x, self.area.y))


class Button(Label):

    def __init__(self, area: Tuple[Union[float, int], Union[float, int], Union[float, int], Union[float, int]] = (
            0, 0, 0, 0)):
        super().__init__(area)

    def render(self, surface: pygame.Surface) -> None:
        if self.enabled:
            super().render(surface)

    def act(self):
        # TODO: Check if button is pressed
        pass
