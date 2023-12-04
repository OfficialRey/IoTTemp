import math

from engine.core.vector import Vector


class CollisionInformation:

    def __init__(self, direction: Vector = Vector(), distance: float = math.inf, collision_radius: float = -math.inf):
        self.direction = direction
        self.distance = distance
        self.collision_radius = collision_radius
        self.hit = self.distance <= self.collision_radius

    def is_hit(self) -> bool:
        return self.hit

    def get_direction(self) -> Vector:
        return self.direction

    def get_distance(self) -> float:
        return self.distance

    def get_collision_radius(self):
        return self.collision_radius
