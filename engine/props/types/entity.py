from engine.core.vector import Vector
from engine.graphics.textures.atlas import AnimationAtlas
from engine.props.types.sprite import Sprite


class Entity(Sprite):

    def __init__(self, world, animation_atlas: AnimationAtlas, max_health: int, attack: int, defense: int,
                 max_speed: float,
                 acceleration: float, position: Vector = Vector(), velocity: Vector = Vector()):
        super().__init__(animation_atlas, position, velocity, max_speed, acceleration)
        self.max_health = max_health
        self.health = self.max_health
        self.attack = attack
        self.defense = defense
        self.world = world

    def _act(self, delta_time: float) -> None:
        raise NotImplementedError("Implement a behaviour for this props!")

    def update(self, delta_time: float):
        # Animation update
        self._act(delta_time)
        super().update(delta_time)
