from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.bullet.bullet import Bullet
from engine.props.data import UnitData
from engine.props.enemy.enemy import Enemy
from engine.props.player.player import Player
from engine.props.types.sprite import Sprite


class CentipedeHead(Enemy):

    def __init__(self, animation_atlas: AnimationAtlas, position: Vector):
        super().__init__(animation_atlas, UnitData.CENTIPEDE_HEAD, position)

    def run_behaviour(self, world, delta_time: float):
        target = world.player
        self.accelerate((target.get_center_position() - self.get_center_position()).normalize(), delta_time)
        self.animate_generic()

    def on_hit(self):
        pass

    def on_death(self):
        pass

    def on_attack(self):
        pass

    def on_collision(self, other: Sprite):
        if not isinstance(other, Bullet):
            return
        if not isinstance(other.owner, Player):
            return

        # The player shot me
        self.damage(other.bullet_type.get_damage())
        other.life_time = 0
