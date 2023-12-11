from engine.graphics.atlas.level import LevelAtlas
from engine.graphics.textures.texture import Texture


class LevelData:

    def __init__(self, texture_atlas: LevelAtlas, world_name: str, width: int = 50, height: int = 50, layers: int = 2):
        # TODO: Add multiple texture layers
        self.world_name = world_name
        self.layers = layers
        self.width = width
        self.height = height
        self.texture_atlas = texture_atlas
        self.level = [[7 for _ in range(width * height)] for _ in range(self.layers)]

    def get_texture(self, x: int, y: int, layer: int) -> Texture:
        if self.get_texture_id(x, y, layer) == -1:
            return None
        return self.texture_atlas.textures[self.get_texture_id(x, y, layer)]

    def get_texture_id(self, x: int, y: int, layer: int) -> int:
        return self.level[layer][self.convert_position(x, y)]

    def place_texture(self, texture_id: int, x: int, y: int, layer: int) -> None:
        self.level[layer][self.convert_position(x, y)] = texture_id

    def save_level(self, path: str) -> None:
        pass

    def convert_position(self, x: int, y: int) -> int:
        return x + self.width * y


def load_level(path: str) -> LevelData:
    pass
