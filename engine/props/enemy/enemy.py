from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.enemy.data import EnemyData
from engine.props.entity import Entity


class Enemy(Entity):

    def __init__(self, animation_atlas: AnimationAtlas, enemy_data: EnemyData):
        super().__init__(animation_atlas, enemy_data.get_health(), enemy_data.get_attack(), enemy_data.get_defense())

    def act(self, delta_time: float):
        self.run_behaviour(delta_time)

    def accelerate(self, acceleration: Vector) -> None:
        super().accelerate(acceleration)

    def _update_sprite(self):
        pass

    def run_behaviour(self, delta_time: float):
        raise NotImplementedError("Must implement generic behaviour")

    def on_hit(self):
        raise NotImplementedError("Must implement on_hit behaviour")

    def on_death(self):
        raise NotImplementedError("Must implement on_death behaviour")

    def on_attack(self):
        raise NotImplementedError("Must implement on_attack behaviour")

    def shoot(self):
        # TODO: Implement
        pass
