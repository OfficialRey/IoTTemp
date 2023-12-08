from enum import Enum


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
    RANGED_ATTACK = 10
    MELEE_ATTACK = 11
    DAMAGED = 12
    DODGE = 13
    DEATH = 14


class AnimationData:

    def __init__(self, animation_type: AnimationType, start_index: int, end_index: int, animation_time: float,
                 loop: bool):
        self.animation_type = animation_type
        self.start_index = start_index
        self.end_index = end_index
        self.length = self.end_index - self.start_index
        self.animation_time = animation_time
        self.loop = loop

    def set_cycle_time(self, time: float):
        self.animation_time = time / self.length

    def copy(self):
        return AnimationData(self.animation_type, self.start_index, self.end_index, self.animation_time, self.loop)
