from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.enemy.data import UnitData
from engine.props.types.unit import Unit


class Enemy(Unit):

    def __init__(self, animation_atlas: AnimationAtlas, enemy_data: UnitData, position: Vector):
        super().__init__(animation_atlas, enemy_data.get_health(), enemy_data.get_attack(), enemy_data.get_defense(),
                         enemy_data.get_max_speed(), enemy_data.get_acceleration(), position)

    def act(self, world, delta_time: float):
        self.run_behaviour(world, delta_time)
