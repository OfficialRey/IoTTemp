from typing import List, Union

from engine.core.vector import Vector
from engine.graphics.atlas.level import LevelAtlas, load_atlas
from engine.graphics.textures.texture import Texture

from json import loads

from engine.world.collision import Collision, load_collision

LAYERS = "layers"
WIDTH = "width"
HEIGHT = "height"
CONTENT = "content"
COLLISION = "collision"
SCALE = "scale"
ATLAS = "atlas"

PLAYER_SPAWN_POINT = 0
ENEMY_SPAWN_POINT = 1


class LevelData:

    def __init__(self, texture_atlas: LevelAtlas, width: int = 50, height: int = 50, layers: int = 2,
                 base_block: int = -1, level_data: List[List[int]] = None, collision: List[Collision] = None):
        # TODO: Add multiple texture layers
        if level_data is None:
            level_data = [[base_block for _ in range(width * height)] for _ in range(layers)]
        if collision is None:
            collision = [Collision() for _ in range(width * height)]

        self.texture_atlas = texture_atlas
        self.layers = layers
        self.width = width
        self.height = height
        self.collision = collision
        self.level = level_data
        self.collision = collision

        self.player_spawn_points = []
        self.enemy_spawn_points = []

        self._load_spawn_points()

    def get_texture(self, x: int, y: int, layer: int) -> Union[None, Texture]:
        texture_id = self.get_texture_id(x, y, layer)
        if texture_id <= ENEMY_SPAWN_POINT:
            return None
        return self.texture_atlas.textures[self.get_texture_id(x, y, layer)]

    def are_coordinates_valid(self, x: int, y: int, layer: int):
        if not (0 <= layer < self.layers):
            return False

        data = self.level[layer]
        position = self.convert_position(x, y)

        if not (0 <= position < len(data)):
            return False

        return True

    def get_texture_id(self, x: int, y: int, layer: int) -> int:
        if not self.are_coordinates_valid(x, y, layer):
            return -1
        return self.level[layer][self.convert_position(x, y)]

    def place_texture(self, texture_id: int, x: int, y: int, layer: int) -> None:
        if not self.are_coordinates_valid(x, y, layer):
            return
        self.level[layer][self.convert_position(x, y)] = texture_id

    def get_collision(self, x: int, y: int) -> Collision:
        position = self.convert_position(x, y)
        if position < 0 or position >= len(self.collision):
            return None
        return self.collision[position]

    def change_collision(self, x: int, y: int, center_position: Vector, radius: float = -1):
        position = self.convert_position(x, y)
        collision = self.collision[position]
        collision.update_center_position(center_position)
        collision.change_collision_shape()
        if radius >= 0:
            collision.radius = radius

    def change_collision_radius(self, x: int, y: int, motion: float):
        position = self.convert_position(x, y)
        collision = self.collision[position]
        collision.radius += motion

    def save_level(self, path: str) -> None:
        # Create JSON object
        storage = {
            ATLAS: self.texture_atlas.get_dict(),
            WIDTH: self.width,
            HEIGHT: self.height,
            LAYERS: self.layers,
            CONTENT: self.level,
            COLLISION: [collision.get_dict() for collision in self.collision]
        }
        with open(path, "w") as file:
            file.write(str(storage))
            file.close()

    def convert_position(self, x: int, y: int) -> int:
        return int(x + self.width * y)

    def _load_spawn_points(self):
        for layer in range(self.layers):
            for x in range(self.width):
                for y in range(self.height):
                    position = Vector(
                        x * self.texture_atlas.scaled_width + self.texture_atlas.scaled_width // 2,
                        y * self.texture_atlas.scaled_height + self.texture_atlas.scaled_height // 2
                    )
                    texture_id = self.get_texture_id(x, y, layer)
                    if texture_id == PLAYER_SPAWN_POINT:
                        self.player_spawn_points.append(position)
                    elif texture_id == ENEMY_SPAWN_POINT:
                        self.enemy_spawn_points.append(position)


def load_level(path: str) -> LevelData:
    with open(path, "r") as file:
        content = loads(file.read().replace("'", '"'))
        file.close()

    return LevelData(
        load_atlas(content[ATLAS]),
        content[WIDTH],
        content[HEIGHT],
        content[LAYERS],
        level_data=content[CONTENT],
        collision=[load_collision(collision) for collision in content[COLLISION]]
    )
