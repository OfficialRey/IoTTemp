from typing import List, Union

from engine.core.vector import Vector
from engine.graphics.atlas.level import LevelAtlas, load_atlas
from engine.graphics.textures.texture import Texture

from json import loads

from engine.world.collision import Collision, load_collision

WORLD = "world"
LAYERS = "layers"
WIDTH = "width"
HEIGHT = "height"
CONTENT = "content"
COLLISION = "collision"
SCALE = "scale"
ATLAS = "atlas"


class LevelData:

    def __init__(self, texture_atlas: LevelAtlas, world_name: str, width: int = 50, height: int = 50, layers: int = 2,
                 base_block: int = -1, level_data: List[List[int]] = None, collision: List[Collision] = None):
        # TODO: Add multiple texture layers
        if level_data is None:
            level_data = [[base_block for _ in range(width * height)] for _ in range(layers)]
        if collision is None:
            collision = [Collision() for _ in range(width * height)]

        self.texture_atlas = texture_atlas
        self.world_name = world_name
        self.layers = layers
        self.width = width
        self.height = height
        self.collision = collision
        self.level = level_data
        self.collision = collision

    def get_texture(self, x: int, y: int, layer: int) -> Union[None, Texture]:
        if self.get_texture_id(x, y, layer) == -1:
            return None
        return self.texture_atlas.textures[self.get_texture_id(x, y, layer)]

    def get_texture_id(self, x: int, y: int, layer: int) -> int:
        return self.level[layer][self.convert_position(x, y)]

    def place_texture(self, texture_id: int, x: int, y: int, layer: int) -> None:
        self.level[layer][self.convert_position(x, y)] = texture_id

    def get_collision(self, x: int, y: int):
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

    def save_level(self, path: str) -> None:
        # Create JSON object
        storage = {
            ATLAS: self.texture_atlas.get_dict(),
            WORLD: self.world_name,
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


def load_level(path: str) -> LevelData:
    with open(path, "r") as file:
        content = loads(file.read().replace("'", '"'))
        file.close()

    return LevelData(
        load_atlas(content[ATLAS]),
        content[WORLD],
        content[WIDTH],
        content[HEIGHT],
        content[LAYERS],
        level_data=content[CONTENT],
        collision=[load_collision(collision) for collision in content[COLLISION]]
    )
