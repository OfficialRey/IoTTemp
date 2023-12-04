from engine.core.vector import Vector
from engine.graphics.atlas.animation import AnimationAtlas
from engine.props.bullet.bullet import Bullet
from engine.props.data import UnitData
from engine.props.enemy.enemy import Enemy
from engine.props.player.player import Player
from engine.props.types.collision import CollisionInformation
from engine.props.types.sprite import Sprite


class CentipedeHead(Enemy):

    def __init__(self, atlas: AnimationAtlas, center_position: Vector):
        super().__init__(atlas, UnitData.CENTIPEDE_HEAD, center_position)

    def run_behaviour(self, world, delta_time: float):
        target = world.player
        self.accelerate((target.center_position - self.center_position).normalize(), delta_time)
        self.animate_generic()

    def on_hit(self):
        pass

    def on_death(self):
        pass

    def on_attack(self):
        pass

    def on_collision(self, other: Sprite, collision_info: CollisionInformation):
        if not isinstance(other, Bullet):
            return
        if not isinstance(other.owner, Player):
            return

        # The player shot me
        self.damage(other.get_attack(), collision_info)
        other.life_time = 0
