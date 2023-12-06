from typing import List

from engine.graphics.atlas.atlas import Atlas
from engine.graphics.textures.texture import Texture
from engine.util.debug import print_debug


class LevelAtlas(Atlas):

    def __init__(self, path: str, file_name: str, sprite_width: int, sprite_height: int):
        super().__init__(path, file_name, sprite_width, sprite_height)

        print_debug(f"Creating level atlas {path}/{file_name}")

        self.textures = self.load_textures()

    def load_textures(self) -> List[Texture]:
        textures = []
        for y in range(self.y_length):
            for x in range(self.x_length):
                texture = Texture(self.surface.subsurface(
                    (x * self.sprite_width, y * self.sprite_height, self.sprite_width, self.sprite_height)))
                if not texture.is_empty():
                    textures.append(texture)
        return textures

    def __getitem__(self, item: int) -> Texture:
        return self.textures[item]
