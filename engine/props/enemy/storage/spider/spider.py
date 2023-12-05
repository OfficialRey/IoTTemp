from engine.core.vector import Vector
from engine.graphics.atlas.animation import AnimationAtlas
from engine.props.data import UnitData
from engine.props.enemy.enemy import ShootingEnemy
from engine.props.weapon.weapon import Weapon

TARGET_DISTANCE = 650


class ShootingSpider(ShootingEnemy):

    def __init__(self, atlas: AnimationAtlas, weapon: Weapon, center_position: Vector):
        super().__init__(atlas, weapon, UnitData.SHOOTING_SPIDER, center_position)

    def run_behaviour(self, world, delta_time: float):
        target = world.player
        vector = target.center_position - self.center_position
        distance = vector.magnitude()

        acceleration = vector.normalize() * (distance - TARGET_DISTANCE)
        self.accelerate(acceleration, delta_time)
