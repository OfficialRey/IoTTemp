from engine.core.vector import Vector
from engine.world.collision import Collision, CollisionShape

COLLISION_SPEED_FACTOR = 0.25

ACCELERATION_FACTOR = 500

VELOCITY_DECAY = 0.99


class Movable:

    def __init__(self, max_speed: float = 0, acceleration: float = 0, center_position: Vector = Vector(),
                 velocity: Vector = Vector(), collision=Collision()):
        super().__init__()
        # From now on: center position
        self.collision = collision
        self.center_position = center_position
        self.velocity = velocity
        self.max_speed = max_speed
        self.acceleration = acceleration

    def accelerate_uncapped(self, acceleration: Vector):
        self.velocity += acceleration * ACCELERATION_FACTOR
        self.cap_velocity()

    def accelerate_normalized(self, acceleration: Vector, delta_time: float) -> None:
        self.velocity += acceleration.normalize() * self.acceleration * delta_time * ACCELERATION_FACTOR
        self.cap_velocity()

    def cap_velocity(self):
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    def update(self, world, delta_time: float) -> None:
        self.center_position += self.velocity * delta_time / world.get_camera_zoom()
        self.collision.center_position = self.center_position

        self.handle_world_collision(world)

    def handle_world_collision(self, world):
        x_pos = self.center_position.x // world.texture_atlas.scaled_width
        y_pos = self.center_position.y // world.texture_atlas.scaled_height

        for x in range(-1, 2):
            for y in range(-1, 2):
                # Find the closest collision object
                collision = world.level_data.get_collision(x_pos + x, y_pos + y)
                if collision is None or collision.shape == CollisionShape.NONE:
                    continue
                if self.collision.collides_with(collision).hit:
                    self.on_world_collide(collision)
                    self.fix_collision(collision)

    def fix_collision(self, collision: Collision, step: float = 10):
        # Get Vector of Object->Self
        vector = self.collision.center_position - collision.center_position

        # Move unit away from object
        self.center_position += vector.normalize() * step

        # Adjust own velocity to erase movement towards object
        me_to_object = vector.inverse().normalize()
        speed = self.velocity.magnitude() * COLLISION_SPEED_FACTOR
        self.velocity = (self.velocity.normalize() - me_to_object.normalize()) * speed

        # Update own collision object
        self.collision.center_position = self.center_position

    def on_world_collide(self, collision: Collision):
        pass
