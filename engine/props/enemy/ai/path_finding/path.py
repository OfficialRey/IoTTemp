from typing import List

from engine.core.vector import Vector
from engine.world.collision import Collision

EMPTY = 0
BLOCKED = 1

DIAGONAL_COST = 14
HORIZONTAL_COST = 10


class Path:

    def __init__(self, world, start_unit_position: Vector, target_unit_position: Vector):
        self.world = world
        self.grid = self.world.grid
        self.start_position = start_unit_position
        self.target_position = target_unit_position
        self.path: List[Node] = self.grid.find_path(self.start_position, self.target_position)

    def get_target_direction(self, unit):
        if self.path is None or len(self.path) <= 1:
            return Vector()
        travel_node = self.path[1]
        return travel_node.get_center_position(self.world) - unit.center_position


class Node:

    def __init__(self, blocked: bool, grid_position: Vector):
        self.blocked = blocked
        self.grid_position = grid_position.as_int()

        self.g_cost = 0
        self.h_cost = 0
        self.parent_node = None

    def get_f_cost(self):
        return self.g_cost + self.h_cost

    def get_distance(self, other):
        x_distance = abs(self.grid_position.x - other.grid_position.x)
        y_distance = abs(self.grid_position.y - other.grid_position.y)
        difference = abs(x_distance - y_distance)

        if x_distance > y_distance:
            return DIAGONAL_COST * y_distance + HORIZONTAL_COST * difference
        return DIAGONAL_COST * x_distance + HORIZONTAL_COST * difference

    def get_center_position(self, world):
        return self.grid_position * \
            Vector(world.texture_atlas.scaled_width, world.texture_atlas.scaled_height) + \
            Vector(world.texture_atlas.scaled_width // 2, world.texture_atlas.scaled_height // 2)

    def __str__(self):
        return f"Node(X: {self.grid_position.x}, Y: {self.grid_position.y})"


class Grid:

    def __init__(self, world, ):
        self.world = world
        self.grid_size = Vector(world.level_data.width, world.level_data.height).as_int()
        self.grid_content = []

        self._create_grid()

    def _create_grid(self):
        self.grid_content = [[None for _ in range(self.grid_size.x)] for _ in range(self.grid_size.y)]
        for x in range(self.grid_size.x):
            for y in range(self.grid_size.y):
                collision: Collision = self.world.level_data.get_collision(x, y)
                self.grid_content[x][y] = Node(bool(collision.shape.value), Vector(x, y))

    def get_node(self, unit_position: Vector) -> Node:
        node_position = (unit_position / Vector(self.world.texture_atlas.scaled_width,
                                                self.world.texture_atlas.scaled_height)).as_int()
        return self.grid_content[node_position.x][node_position.y]

    def get_neighbours(self, node: Node) -> List[Node]:
        neighbours = []

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == y == 0:
                    continue

                check_x = node.grid_position.x + x
                check_y = node.grid_position.y + y

                if 0 <= check_x < self.grid_size.x and 0 <= check_y < self.grid_size.y:
                    neighbours.append(self.grid_content[check_x][check_y])

        return neighbours

    def find_path(self, start_unit_position: Vector, target_unit_position: Vector) -> List[Node]:
        start_node = self.get_node(start_unit_position)
        target_node = self.get_node(target_unit_position)

        open_nodes: List[Node] = [start_node]
        closed_nodes: List[Node] = []

        while len(open_nodes) > 0:

            # Get Node with lowest F Cost
            current_node = open_nodes[0]
            for i in range(1, len(open_nodes)):
                if open_nodes[i].get_f_cost() < current_node.get_f_cost() or \
                        open_nodes[i].get_f_cost() == current_node.get_f_cost() and \
                        open_nodes[i].h_cost < current_node.h_cost:
                    current_node = open_nodes[i]

            open_nodes.remove(current_node)
            closed_nodes.append(current_node)

            if current_node == target_node:
                return trace_path(start_node, target_node)

            for neighbour in self.get_neighbours(current_node):
                if neighbour.blocked or neighbour in closed_nodes:
                    continue

                movement_cost = current_node.g_cost + current_node.get_distance(neighbour)
                if movement_cost < neighbour.g_cost or neighbour not in open_nodes:
                    neighbour.g_cost = movement_cost
                    neighbour.h_cost = target_node.get_distance(neighbour)
                    neighbour.parent_node = current_node

                    if neighbour not in open_nodes:
                        open_nodes.append(neighbour)


def trace_path(start_node: Node, target_node: Node):
    path = []
    current_node = target_node

    while current_node is not start_node:
        path.append(current_node)
        current_node = current_node.parent_node

    path.reverse()
    return path
