import math
import random
from typing import Tuple

NUMBER_TYPE = (int, float, complex)

X = "x"
Y = "y"


class Vector:

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def inverse(self):
        return Vector(-self.x, -self.y)

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        magnitude = self.magnitude()
        if magnitude > 0:
            return Vector(self.x / magnitude, self.y / magnitude)
        return Vector(0, 0)

    def distance(self, other) -> float:
        return (other - self).magnitude()

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def angle(self, other):
        dot_product = self.dot_product(other)
        len_product = self.magnitude() * other.magnitude()
        if len_product == 0:
            return 0
        return math.degrees(math.acos(dot_product / len_product))

    def rotate_counter_clockwise(self, theta: float):
        theta = math.radians(theta)
        cs = math.cos(theta)
        sn = math.sin(theta)
        return Vector(self.x * cs - self.y * sn, self.x * sn + self.y * cs)

    def as_tuple(self) -> Tuple[float, float]:
        return self.x, self.y

    def as_int(self):
        return Vector(int(self.x), int(self.y))

    def get_dict(self):
        return {
            X: self.x,
            Y: self.y
        }

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            raise RuntimeError("Can only add two vectors!")

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            raise RuntimeError("Can only subtract two vectors!")

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        elif isinstance(other, NUMBER_TYPE):
            return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)
        elif isinstance(other, NUMBER_TYPE):
            return Vector(self.x / other, self.y / other)

    def __str__(self):
        return "Vector{" f"{self.x}, {self.y}" "}"

    @classmethod
    def random(cls):
        return Vector(random.random(), random.random()).normalize()

    @classmethod
    def up(cls):
        return Vector(0, -1)


def load_vector(vector_data: dict) -> Vector:
    return Vector(
        vector_data[X],
        vector_data[Y]
    )


if __name__ == '__main__':
    # Vector rotation test
    vector = Vector(1, 0)
    for rotation in range(0, 360, 1):
        print(f"Rotation: {rotation} | Vector: {vector.rotate_counter_clockwise(rotation)}")

    # Angle Test

    for x, y in zip([i / 10 for i in range(11)], [i / 10 for i in range(10, -1, -1)]):
        angle = Vector.up().angle(Vector(x, y))
        print(x, y)
        print(angle)
    print()

    for x, y in zip([-i / 10 for i in range(10, -1, -1)], [-i / 10 for i in range(11)]):
        angle = Vector.up().angle(Vector(x, y))
        print(x, y)
        print(angle)
