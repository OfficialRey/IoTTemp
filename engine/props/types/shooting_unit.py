from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.bullet.bullet import Bullet, BulletType
from engine.props.types.unit import Unit


class ShootingUnit(Unit):

    def __init__(self, world, animation_atlas: AnimationAtlas, max_health: int, attack: int, defense: int,
                 max_speed: float, acceleration: float, position: Vector = Vector(), velocity: Vector = Vector()):
        super().__init__(world, animation_atlas, max_health, attack, defense, position, velocity, max_speed,
                         acceleration)

    def shoot_bullet(self, animation_atlas: AnimationAtlas, bullet_type: BulletType, direction: Vector):
        bullet = Bullet(animation_atlas, self, bullet_type, self.position, direction)
        self.world.add_bullet(bullet)

    def act(self, delta_time: float):
        raise NotImplementedError()
