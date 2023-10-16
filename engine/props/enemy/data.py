from enum import Enum

from engine.graphics.textures.texture_manager import TextureManager

ANIMATION = 0


class EnemyData(Enum):
    # Syntax: Base Max Health, Base Attack, Base Defense

    CACO_DEMON = (12, 12, 12)
    CENTIPEDE = (30, 6, 2)
    _CENTIPEDE_BODY = (12, 2, 0)

    def get_health(self):
        return self.value[0]

    def get_attack(self):
        return self.value[1]

    def get_defense(self):
        return self.value[2]

    def get_enemy(self, texture_manager: TextureManager):
        # TODO: Return actual entity object
        if self == EnemyData.CACO_DEMON:
            return None
        elif self == EnemyData.CENTIPEDE:
            return None
