from typing import List

import pygame.event

from engine.core.window import Window
from engine.game_info.game_info import GameInformation
from engine.graphics.gui.widget import Widget
from engine.util.util import show_cursor


class Menu:

    def __init__(self):
        self.widgets: List[Widget] = []
        show_cursor()

    def run(self, game_info: GameInformation):
        for widget in self.widgets:
            widget.update(game_info)

    def render(self, window: Window):
        window.fill()
        for widget in self.widgets:
            widget.render(window.surface)
        pygame.display.flip()

    def add_widget(self, widget: Widget):
        if widget not in self.widgets:
            self.widgets.append(widget)

    def remove_widget(self, widget: Widget):
        if widget in self.widgets:
            self.widgets.remove(widget)
