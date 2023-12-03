import os

import pygame

from engine.editor.level_editor import LevelEditor
from engine.util.resources import set_application_path
from game.game import TopDownGame


def init():
    # Initialise required fields
    set_application_path(os.path.dirname(__file__))
    pygame.init()
    pygame.display.init()


def start(level_editor: bool = False):
    init()
    if not level_editor:
        game = TopDownGame()
        game.run()
    else:
        editor = LevelEditor()
        editor.run()


if __name__ == '__main__':
    start(False)
