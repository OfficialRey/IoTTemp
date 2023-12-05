from enum import Enum

ANIMATION = 0


class UnitData(Enum):
    # Syntax: Base Max Health, Base Attack, Base Defense, Max Speed, Acceleration

    NONE = (0, 0, 0, 0, 0)
    PLAYER = (100, 0, 0, 2700, 6)

    CENTIPEDE_HEAD = (8, 8, 0, 1500, 1200)
    CENTIPEDE_BODY = (10, 2, 0, 1500, 1200)

    SHOOTING_SPIDER = (12, 4, 0, 1200, 4)

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
