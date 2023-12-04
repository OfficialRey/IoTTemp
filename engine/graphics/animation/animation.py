import os
from enum import Enum
from typing import List

import pygame

from engine.core.vector import Vector
from engine.graphics.textures.texture import Texture
from engine.util.debug import print_debug
from engine.util.resources import get_resource_path


class AnimationType(Enum):
    GENERIC = -1
    IDLE = 0
    WALKING_GENERAL = 1

    # Compass
    WALKING_N = 2
    WALKING_S = 3
    WALKING_W = 4
    WALKING_E = 5

    WALKING_NE = 6
    WALKING_SE = 7
    WALKING_SW = 8
    WALKING_NW = 9

    # Actions
    ATTACK = 10
    DAMAGED = 11
    DODGE = 12
    DEATH = 13


class AnimationData:

    def __init__(self, animation_type: AnimationType, start_index: int, end_index: int, animation_time: float,
                 loop: bool):
        self.animation_type = animation_type
        self.start_index = start_index
        self.stop_index = end_index
        self.length = self.stop_index - self.start_index
        self.animation_time = animation_time
        self.loop = loop
