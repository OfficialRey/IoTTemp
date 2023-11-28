from engine.graphics.textures.texture_manager import TextureManager
from engine.props.enemy.data import EnemyData
from engine.props.enemy.enemy import Enemy


class Centipede(Enemy):

    def __init__(self, texture_manager: TextureManager):
        super().__init__(texture_manager.centipede, EnemyData.CENTIPEDE)
        self.body_texture = texture_manager.centipede_body
        self.body = []

    def run_behaviour(self, delta_time: float):
        pass

    def on_hit(self):
        pass

    def on_death(self):
        pass

    def on_attack(self):
        pass
