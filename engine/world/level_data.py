from engine.graphics.atlas.level import LevelAtlas
from engine.graphics.textures.texture import Texture

from random import random


class LevelData:

    def __init__(self, texture_atlas: LevelAtlas, world_name: str, width: int = 50, height: int = 50):
        # TODO: Add multiple texture layers
        self.world_name = world_name
        self.width = width
        self.height = height
        self.texture_atlas = texture_atlas
        self.level = [5 for _ in range(width * height)]

    def get_texture(self, x: int, y: int) -> Texture:
        return self.texture_atlas.textures[self.get_texture_id(x, y)]

    def get_texture_id(self, x: int, y: int) -> int:
        return self.level[self.convert_position(x, y)]

    def place_texture(self, texture_id: int, x: int, y: int) -> None:
        self.level[self.convert_position(x, y)] = texture_id

    def save_level(self, path: str) -> None:
        pass

    def convert_position(self, x: int, y: int) -> int:
        return x + self.width * y


def load_level(path: str) -> LevelData:
    pass
