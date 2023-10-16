from engine.core.engine import Engine
from engine.graphics.textures.texture_manager import TextureManager
from engine.world.level_data import LevelData
from engine.world.world import World


class TopDownGame:

    def __init__(self):
        self.engine = Engine(max_fps=144)
        self.texture_manager = TextureManager()
        self.world = World(
            self.texture_manager,
            LevelData(self.texture_manager.level_textures, "Test", 512, 512),
            self.engine.window,
            1
        )

    def run(self):
        self.engine.run(self.world)
