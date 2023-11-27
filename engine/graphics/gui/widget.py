from typing import Tuple, Union

import pygame

WHITE = (255, 255, 255)

BACKGROUND_SIZE = 5


class Widget:

    def __init__(self, area: Tuple[Union[float, int], Union[float, int], Union[float, int], Union[float, int]]):
        self.area = pygame.Rect(area)
        self.background_area = pygame.Rect(area[0] - BACKGROUND_SIZE, area[1] - BACKGROUND_SIZE,
                                           area[2] + BACKGROUND_SIZE * 2, area[2] + BACKGROUND_SIZE * 2)
        self.enabled = True

    def set_area(self, area: Tuple[Union[float, int], Union[float, int], Union[float, int], Union[float, int]]):
        self.area = pygame.Rect(area)
        self.background_area = pygame.Rect(area[0] - BACKGROUND_SIZE, area[1] - BACKGROUND_SIZE,
                                           area[2] + BACKGROUND_SIZE * 2, area[2] + BACKGROUND_SIZE * 2)

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
            surface.fill(self.background_color, self.background_area)
        if self.render_content is not None:
            surface.blit(self.render_content, (self.area.x, self.area.y))


class Button(Label):

    def __init__(self, area: Tuple[Union[float, int], Union[float, int], Union[float, int], Union[float, int]] = (
            0, 0, 0, 0)):
        super().__init__(area)
        self.pressed = False

    def render(self, surface: pygame.Surface) -> None:
        if self.enabled:
            super().render(surface)

    def act(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            x_pos, y_pos = pygame.mouse.get_pos()
            if self.area.x <= x_pos <= self.area.x + self.area.width and \
                    self.area.y <= y_pos <= self.area.y + self.area.height:
                self.pressed = event.type == pygame.MOUSEBUTTONDOWN
                if self.pressed:
                    self.on_press()
                else:
                    self.on_release()

    def on_press(self):
        raise NotImplementedError()

    def on_release(self):
        raise NotImplementedError()
