from engine.graphics.gui.menu.menu_buttons import StartButton, QuitButton
from engine.menu.menu import Menu

BORDER_DISTANCE = 0.2


class StartMenu(Menu):

    def __init__(self, engine):
        super().__init__()

        start_x, width = engine.window.get_width() * BORDER_DISTANCE, engine.window.get_width() * (
                1 - BORDER_DISTANCE * 2)

        self.add_widget(StartButton((start_x, 100, width, 100), engine))
        self.add_widget(QuitButton((start_x, 300, width, 100)))


class PauseMenu(Menu):
    pass
