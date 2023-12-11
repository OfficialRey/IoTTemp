from typing import List

from engine.graphics.atlas.level import LevelAtlas
from engine.graphics.textures.texture import Texture

from json import loads

WORLD = "world"
LAYERS = "layers"
WIDTH = "width"
HEIGHT = "height"
CONTENT = "content"
TEXTURE_ATLAS = "atlas"

ATLAS_PATH = "path"
ATLAS_FILE = "file"
ATLAS_SPRITE_WIDTH = "sprite_width"
ATLAS_SPRITE_HEIGHT = "sprite_height"


class LevelData:

    def __init__(self, texture_atlas: LevelAtlas, world_name: str, width: int = 50, height: int = 50, layers: int = 2,
                 base_block: int = -1, level_data: List[List[int]] = None):
        # TODO: Add multiple texture layers
        if level_data is None:
            level_data = [[base_block for _ in range(width * height)] for _ in range(layers)]

        self.texture_atlas = texture_atlas
        self.world_name = world_name
        self.layers = layers
        self.width = width
        self.height = height
        self.level = level_data

    def get_texture(self, x: int, y: int, layer: int) -> Texture:
        if self.get_texture_id(x, y, layer) == -1:
            return None
        return self.texture_atlas.textures[self.get_texture_id(x, y, layer)]

    def get_texture_id(self, x: int, y: int, layer: int) -> int:
        return self.level[layer][self.convert_position(x, y)]

    def place_texture(self, texture_id: int, x: int, y: int, layer: int) -> None:
        self.level[layer][self.convert_position(x, y)] = texture_id

    def save_level(self, path: str) -> None:
        # Create JSON object
        atlas = {
            ATLAS_PATH: self.texture_atlas.path,
            ATLAS_FILE: self.texture_atlas.file_name,
            ATLAS_SPRITE_WIDTH: self.texture_atlas.sprite_width,
            ATLAS_SPRITE_HEIGHT: self.texture_atlas.sprite_height
        }
        storage = {
            TEXTURE_ATLAS: atlas,
            WORLD: self.world_name,
            WIDTH: self.width,
            HEIGHT: self.height,
            LAYERS: self.layers,
            CONTENT: self.level
        }
        with open(path, "w") as file:
            file.write(str(storage))
            file.close()

    def convert_position(self, x: int, y: int) -> int:
        return x + self.width * y


def load_level(path: str) -> LevelData:
    with open(path, "r") as file:
        content = loads(file.read().replace("'", '"'))
        file.close()

    atlas_data = content[TEXTURE_ATLAS]
    atlas = LevelAtlas(
        atlas_data[ATLAS_PATH],
        atlas_data[ATLAS_FILE],
        atlas_data[ATLAS_SPRITE_WIDTH],
        atlas_data[ATLAS_SPRITE_HEIGHT]
    )

    return LevelData(
        atlas,
        content[WORLD],
        content[WIDTH],
        content[HEIGHT],
        content[LAYERS],
        level_data=content[CONTENT]
    )
