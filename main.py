import os

import pygame

from engine.util.resources import set_application_path
from game.game import TopDownGame


def init():
    # Initialise required fields
    set_application_path(os.path.dirname(__file__))
    pygame.init()
    pygame.display.init()


if __name__ == '__main__':
    init()
    game = TopDownGame()
    game.run()
