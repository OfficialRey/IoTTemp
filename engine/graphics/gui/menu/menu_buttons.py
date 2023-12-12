from typing import Tuple

import pygame.mouse

from engine.graphics.gui.widget import Button, WHITE
from engine.sound.game_sound import GameMusic
from engine.util.util import show_cursor

BACKGROUND_COLOR = 142, 33, 33
HOVER_COLOR = 224, 97, 1
BORDER_COLOR = 249, 198, 41


class StartButton(Button):

    def __init__(self, area: Tuple[int, int, int, int], engine):
        super().__init__(area, "Start Game", WHITE, BACKGROUND_COLOR, BORDER_COLOR, HOVER_COLOR,
                         sound_engine=engine.sound_engine)
        self.engine = engine

    def on_press(self):
        self.engine.current_menu = None
        self.engine.sound_engine.play_music(GameMusic.DEFAULT)
        show_cursor(False)

    def on_release(self):
        pass


class QuitButton(Button):

    def __init__(self, area: Tuple[int, int, int, int], engine):
        super().__init__(area, "Quit To Desktop", WHITE, BACKGROUND_COLOR, BORDER_COLOR, HOVER_COLOR,
                         sound_engine=engine.sound_engine)

    def on_press(self):
        exit(0)

    def on_release(self):
        pass
