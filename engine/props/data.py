from enum import Enum

ANIMATION = 0


class UnitData(Enum):
    # Syntax: Base Max Health, Base Attack, Base Defense, Max Speed, Acceleration, Shot Delay

    NONE = (0, 0, 0, 0, 0, 0)
    PLAYER = (100, 0, 0, 2700, 6, 0)

    CENTIPEDE = (6, 4, 0, 1500, 4, 0)
    CENTIPEDE_BODY = (12, 2, 0, 1550, 30, 0)
    SHOOTING_SPIDER = (12, 2, 0, 1200, 4, 2)

    def get_health(self):
        return self.value[0]

    def get_attack(self):
        return self.value[1]

    def get_defense(self):
        return self.value[2]

    def get_max_speed(self):
        return self.value[3]

    def get_acceleration(self):
        return self.value[4]

    def get_shot_delay(self):
        return self.value[5]
