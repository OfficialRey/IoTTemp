from enum import Enum

from engine.graphics.textures.texture_manager import TextureManager

ANIMATION = 0


class EnemyData(Enum):
    # Syntax: Base Max Health, Base Attack, Base Defense, Max Speed

    CACO_DEMON = (12, 12, 12, 1)
    CENTIPEDE = (30, 6, 2, 200)
    _CENTIPEDE_BODY = (12, 2, 0, 200)

    def get_health(self):
        return self.value[0]

    def get_attack(self):
        return self.value[1]

    def get_defense(self):
        return self.value[2]

    def get_max_speed(self):
        if isinstance(self.value, tuple):
            if len(self.value) > 2:
                return self.value[3]
        return 0

    def get_enemy(self, texture_manager: TextureManager):
        # TODO: Return actual entity object
        if self == EnemyData.CACO_DEMON:
            return None
        elif self == EnemyData.CENTIPEDE:
            return None
