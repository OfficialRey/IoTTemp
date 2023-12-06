from engine.core.vector import Vector


class Movable:

    def __init__(self, max_speed: float = 0, acceleration: float = 0, center_position: Vector = Vector(),
                 velocity: Vector = Vector()):
        super().__init__()
        # From now on: center position
        self.center_position = center_position
        self.velocity = velocity
        self.max_speed = max_speed
        self.acceleration = acceleration

    def accelerate(self, acceleration: Vector, delta_time: float) -> None:
        self.velocity += acceleration * self.acceleration * delta_time
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    def update(self, world, delta_time: float) -> None:
        self.center_position += self.velocity * delta_time / world.get_camera_zoom()
