from typing import List

import pygame.event

from engine.core.window import Window
from engine.graphics.gui.widget import Widget


class Menu:

    def __init__(self):
        self.widgets: List[Widget] = []

    def run(self):
        for event in pygame.event.get():
            for widget in self.widgets:
                widget.update(event)

    def render(self, window: Window):
        for widget in self.widgets:
            widget.render(window.surface)

    def add_widget(self, widget: Widget):
        if widget not in self.widgets:
            self.widgets.append(widget)

    def remove_widget(self, widget: Widget):
        if widget in self.widgets:
            self.widgets.remove(widget)
