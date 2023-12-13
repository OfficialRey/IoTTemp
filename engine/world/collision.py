from enum import IntEnum

import pygame
from pygame.math import clamp

import math

from engine.core.vector import Vector, load_vector

CENTER_POSITION = "center_position"
RADIUS = "radius"
SHAPE = "shape"


class CollisionShape(IntEnum):
    NONE = 0,
    CIRCLE = 1,
    RECTANGLE = 2


class CollisionInformation:

    def __init__(self, direction: Vector = Vector(), center_distance: float = math.inf, hit: bool = False,
                 collision_distance: float = 0):
        self.direction = direction
        self.center_distance = center_distance
        self.collision_distance = collision_distance
        self.hit = hit


class Collision:

    def __init__(self, center_position: Vector = Vector(), radius: float = 0,
                 shape: CollisionShape = CollisionShape.NONE):
        self.center_position = center_position
        self.rectangle = pygame.Rect(self.center_position.x - radius, self.center_position.y - radius, radius * 2,
                                     radius * 2)
        self.radius = radius
        self.shape = shape

    def update_center_position(self, center_position: Vector):
        self.center_position = center_position
        self.rectangle = pygame.Rect(
            self.center_position.x - self.radius,
            self.center_position.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def collides_with(self, other) -> CollisionInformation:
        if self.shape == CollisionShape.NONE or other.shape == CollisionShape.NONE:
            return CollisionInformation()

        if self.shape == other.shape == CollisionShape.CIRCLE:
            return intersect_circle_circle(self, other)

        if self.shape == other.shape == CollisionShape.RECTANGLE:
            return intersect_rectangle_rectangle(self, other)

        circle = self if self.shape == CollisionShape.CIRCLE else other
        rectangle = self if self.shape == CollisionShape.RECTANGLE else other
        return intersect_circle_rectangle(circle, rectangle)

    def change_collision_shape(self):
        shape = self.shape + 1
        if shape >= len(CollisionShape):
            shape = 0
        self.shape = CollisionShape(shape)

    def get_dict(self):
        return {
            CENTER_POSITION: self.center_position.get_dict(),
            RADIUS: self.radius,
            SHAPE: int(self.shape)
        }


def intersect_circle_circle(circle, other) -> CollisionInformation:
    vector = circle.center_position - other.center_position
    center_distance = vector.magnitude()
    collision_distance = circle.radius + other.radius - center_distance
    hit = center_distance < circle.radius + other.radius
    return CollisionInformation(vector, center_distance, hit, collision_distance)


def intersect_rectangle_rectangle(rectangle, other) -> CollisionInformation:
    vector = rectangle.center_position - other.center_position
    distance = vector.magnitude()
    hit = rectangle.rectangle.colliderect(other.rectangle)
    return CollisionInformation(vector, distance, hit)


def intersect_circle_rectangle(circle, rectangle) -> CollisionInformation:
    closest_x = clamp(circle.center_position.x, rectangle.rectangle.left, rectangle.rectangle.right)
    closest_y = clamp(circle.center_position.y, rectangle.rectangle.top, rectangle.rectangle.bottom)

    x_distance = circle.center_position.x - closest_x
    y_distance = circle.center_position.y - closest_y

    distance_squared = x_distance ** 2 + y_distance ** 2

    vector = circle.center_position - rectangle.center_position
    distance = vector.magnitude()
    hit = distance_squared < circle.radius ** 2
    return CollisionInformation(vector, distance, hit)


def load_collision(collision_data: dict) -> Collision:
    return Collision(
        load_vector(collision_data[CENTER_POSITION]),
        collision_data[RADIUS],
        CollisionShape(collision_data[SHAPE])
    )
