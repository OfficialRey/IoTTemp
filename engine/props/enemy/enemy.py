from abc import ABC

from engine.core.vector import Vector
from engine.graphics.atlas.animation import AnimationAtlas
from engine.props.data import UnitData
from engine.props.types.unit import ShootingUnit, MeleeUnit
from engine.props.weapon.weapon import Weapon


class ShootingEnemy(ShootingUnit, ABC):

    def __init__(self, atlas: AnimationAtlas, weapon: Weapon, enemy_data: UnitData, center_position: Vector):
        super().__init__(atlas, weapon, enemy_data.get_health(), enemy_data.get_attack(),
                         enemy_data.get_defense(), enemy_data.get_max_speed(), enemy_data.get_acceleration(),
                         center_position)


class MeleeEnemy(MeleeUnit, ABC):

    def __init__(self, atlas: AnimationAtlas, max_health: int, attack: int, defense: int, max_speed: float,
                 acceleration: float):
        super().__init__(atlas, max_health, attack, defense, max_speed, acceleration)
