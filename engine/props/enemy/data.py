from enum import Enum

ANIMATION = 0


class UnitData(Enum):
    # Syntax: Base Max Health, Base Attack, Base Defense, Shot Delay, Max Speed, Acceleration

    CACO_DEMON = (12, 12, 0, 0, 12, 1)
    CENTIPEDE = (30, 6, 0, 0, 28, 0.5)
    CENTIPEDE_BODY = (12, 2, 0, 0, 30, 1)
    PLAYER = (100, 20, 20, 0.2, 55, 0.003)

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
