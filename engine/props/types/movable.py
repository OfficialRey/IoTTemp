from engine.core.vector import Vector


class Movable:

    def __init__(self, position: Vector = Vector(), velocity: Vector = Vector(), max_speed: float = 0,
                 acceleration: float = 0):
        super().__init__()
        self.position = position
        self.velocity = velocity
        self.max_speed = max_speed
        self.acceleration = acceleration

    def accelerate(self, acceleration: Vector) -> None:
        self.velocity += acceleration * self.acceleration
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    def update(self, delta_time: float) -> None:
        self.position += self.velocity * delta_time
