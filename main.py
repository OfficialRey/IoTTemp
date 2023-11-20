import os

import pygame

from engine.util.resources import set_application_path
from game.game import TopDownGame


def init():
    # Initialise required fields
    set_application_path(os.path.dirname(__file__))
    pygame.init()
    pygame.display.init()


def start():
    init()
    game = TopDownGame()
    game.run()


if __name__ == '__main__':
    start()
