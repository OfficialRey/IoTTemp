from engine.core.vector import Vector
from engine.graphics.atlas.animation import AnimationAtlas
from engine.props.bullet.bullet import Bullet
from engine.props.data import UnitData
from engine.props.enemy.enemy import MeleeEnemy
from engine.props.player.player import Player
from engine.props.types.sprite import Sprite
from engine.world.collision import CollisionInformation


class CentipedeHead(MeleeEnemy):

    def __init__(self, world, sound_mixer, core, atlas: AnimationAtlas, center_position: Vector):
        super().__init__(sound_mixer, atlas, world, UnitData.CENTIPEDE_HEAD, center_position)
        self.core = core

    def run_behaviour(self, world, delta_time: float):
        target = world.player
        vector = (target.center_position - self.center_position).normalize()
        self.accelerate(vector, delta_time)
        self.animate_generic()

    def on_collision(self, other: Sprite, collision_info: CollisionInformation):
        if not isinstance(other, Bullet):
            return
        if not isinstance(other.owner, Player):
            return

        # The player shot me
        self.damage(other.get_attack(), collision_info)
        other.life_time = 0
