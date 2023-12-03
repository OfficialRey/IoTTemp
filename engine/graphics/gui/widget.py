from abc import ABC
from typing import Tuple

import pygame

WHITE = (255, 255, 255)

BORDER_SIZE = 5


class Widget(ABC):

    def __init__(self, area: Tuple[int, int, int, int] = (0, 0, 0, 0)):
        self.area = pygame.Rect(area)
        self.border_area = pygame.Rect(area[0] - BORDER_SIZE, area[1] - BORDER_SIZE,
                                       area[2] + BORDER_SIZE * 2, area[3] + BORDER_SIZE * 2)
        self.enabled = True
        self.hovered = False

    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            x_pos, y_pos = pygame.mouse.get_pos()
            if self.area.x <= x_pos <= self.area.x + self.area.width and \
                    self.area.y <= y_pos <= self.area.y + self.area.height:
                self.hovered = True
            else:
                self.hovered = False

    def set_area(self, area: Tuple[int, int, int, int]):
        self.area = pygame.Rect(area)
        self.border_area = pygame.Rect(area[0] - BORDER_SIZE, area[1] - BORDER_SIZE,
                                       area[2] + BORDER_SIZE * 2, area[2] + BORDER_SIZE * 2)

    def render(self, surface: pygame.Surface):
        raise NotImplementedError()


class Label(Widget):

    def __init__(self, area: Tuple[int, int, int, int] = (0, 0, 0, 0),
                 text: str = None, font_color: Tuple[int, int, int] = WHITE,
                 background_color: Tuple[int, int, int] = None, border_color: Tuple[int, int, int] = None,
                 hover_color: Tuple[int, int, int] = None, font: str = "comicsansms"):
        super().__init__(area)
        self.text = text
        self.font = font
        self.sys_font = pygame.font.SysFont(font, self.area.height)
        self.font_color = font_color
        self.background_color = background_color
        self.border_color = border_color
        self.hover_color = hover_color
        self.base_render_content = None
        self.render_content = None

        self.set_text(self.text)

    def update(self, event: pygame.event.Event):
        super().update(event)

    def set_text(self, text: str):
        self.text = text
        self.base_render_content = self.sys_font.render(text, True, self.font_color)
        self.update_content()

    def set_content(self, image: pygame.Surface):
        if image is not None:
            self.base_render_content = image.copy()
            ratio = min(self.area.width, self.area.height) / min(self.base_render_content.get_width(),
                                                                 self.base_render_content.get_height())
            self.render_content = pygame.transform.scale(
                self.base_render_content,
                (self.base_render_content.get_width() * ratio,
                 self.base_render_content.get_height() * ratio)
            )

    def update_content(self):
        self.font = pygame.font.SysFont(self.font, self.area.height)
        self.set_content(self.base_render_content)

    def set_area(self, area: Tuple[int, int, int, int] = (0, 0, 0, 0)):
        super().set_area(area)
        self.update_content()

    def render(self, surface: pygame.Surface) -> None:
        if self.border_color is not None:
            surface.fill(self.border_color, self.border_area)
        if self.background_color is not None:
            surface.fill(self.background_color, self.area)
        if self.hovered and self.hover_color is not None:
            surface.fill(self.hover_color, self.area)
        if self.render_content is not None:
            x = self.area.x + self.area.width // 2 - self.render_content.get_width() // 2
            y = self.area.y + self.area.height // 2 - self.render_content.get_height() // 2
            surface.blit(self.render_content, (x, y))


class Button(Label, ABC):

    def __init__(self, area: Tuple[int, int, int, int] = (0, 0, 0, 0), text: str = None,
                 font_color: Tuple[int, int, int] = WHITE, background_color: Tuple[int, int, int] = None,
                 border_color: Tuple[int, int, int] = None, hover_color: Tuple[int, int, int] = None,
                 font: str = "comicsansms"):
        super().__init__(area, text, font_color, background_color, border_color, hover_color, font)

    def render(self, surface: pygame.Surface) -> None:
        if not self.enabled:
            return
        super().render(surface)

    def update(self, event: pygame.event.Event):
        super().update(event)
        if not self.enabled:
            return

        if self.hovered and event.type == pygame.MOUSEBUTTONDOWN:
            self.on_press()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.on_release()

    def on_press(self):
        raise NotImplementedError()

    def on_release(self):
        raise NotImplementedError()
