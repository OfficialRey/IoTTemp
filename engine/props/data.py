from enum import Enum

ANIMATION = 0


class UnitData(Enum):
    # Syntax: Base Max Health, Base Attack, Base Defense, Shot Delay, Max Speed, Acceleration

    NONE = (0, 0, 0, 0, 0, 0)

    CACO_DEMON = (12, 12, 0, 0, 12, 1)
    CENTIPEDE_HEAD = (30, 6, 0, 0, 1500, 1200)
    CENTIPEDE_BODY = (12, 2, 0, 0, 1500, 1200)
    PLAYER = (100, 0, 0, 0.05, 2700, 6)

    def get_health(self):
        return self.value[0]

    def get_attack(self):
        return self.value[1]

    def get_defense(self):
        return self.value[2]

    def get_shot_delay(self):
        return self.value[3]

    def get_max_speed(self):
        return self.value[4]

    def get_acceleration(self):
        return self.value[5]
