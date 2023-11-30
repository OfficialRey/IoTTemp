from enum import Enum

from engine.graphics.textures.texture_manager import TextureManager

ANIMATION = 0


class UnitData(Enum):
    # Syntax: Base Max Health, Base Attack, Base Defense, Shot Delay, Max Speed, Acceleration

    CACO_DEMON = (12, 12, 0, 0, 12, 1)
    CENTIPEDE = (30, 6, 0, 0, 200, 6)
    CENTIPEDE_BODY = (12, 2, 0, 0, 210, 12)
    PLAYER = (100, 20, 20, 0.2, 400, 0.02)

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

    def get_enemy(self, texture_manager: TextureManager):
        # TODO: Return actual entity object
        if self == UnitData.CACO_DEMON:
            return None
        elif self == UnitData.CENTIPEDE:
            return None
