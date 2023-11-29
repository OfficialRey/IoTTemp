import pygame.sprite

from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.enemy.data import UnitData
from engine.props.types.unit import Unit


class Enemy(Unit):

    def __init__(self, animation_atlas: AnimationAtlas, enemy_data: UnitData):
        super().__init__(animation_atlas, enemy_data.get_health(), enemy_data.get_attack(), enemy_data.get_defense(),
                         enemy_data.get_max_speed(), enemy_data.get_acceleration())

    def act(self, delta_time: float):
        self.run_behaviour(delta_time)

    def run_behaviour(self, delta_time: float):
        raise NotImplementedError("Must implement generic behaviour")

    def on_hit(self):
        raise NotImplementedError("Must implement on_hit behaviour")

    def on_death(self):
        raise NotImplementedError("Must implement on_death behaviour")

    def on_attack(self):
        raise NotImplementedError("Must implement on_attack behaviour")

    def collides_with(self, other: pygame.sprite.Sprite):
        raise NotImplementedError("Must implement collision behaviour")

    def collide_generic(self, other: pygame.sprite.Sprite):
        # TODO: Handle collision
        pass
