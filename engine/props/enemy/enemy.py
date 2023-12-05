from abc import ABC

from engine.core.vector import Vector
from engine.graphics.atlas.animation import AnimationAtlas
from engine.props.bullet.bullet import BulletType
from engine.props.data import UnitData
from engine.props.types.unit import ShootingUnit, MeleeUnit
from engine.sound.game_sound import SoundEngine


class ShootingEnemy(ShootingUnit, ABC):

    def __init__(self, sound_engine: SoundEngine, atlas: AnimationAtlas, bullet_type: BulletType, unit_data: UnitData,
                 center_position: Vector):
        super().__init__(sound_engine, atlas, bullet_type, unit_data.get_health(), unit_data.get_attack(),
                         unit_data.get_defense(), unit_data.get_max_speed(), unit_data.get_acceleration(),
                         unit_data.get_shot_delay(), center_position)


class MeleeEnemy(MeleeUnit, ABC):

    def __init__(self, sound_engine: SoundEngine, atlas: AnimationAtlas, enemy_data: UnitData, center_position: Vector):
        super().__init__(sound_engine, atlas, enemy_data.get_health(), enemy_data.get_attack(),
                         enemy_data.get_defense(),
                         enemy_data.get_max_speed(), enemy_data.get_acceleration(), center_position)
