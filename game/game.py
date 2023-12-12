from engine.core.engine import Engine
from engine.util.debug import print_debug
from engine.world.world import World


class TopDownGame:

    def __init__(self):
        self.engine = Engine(max_fps=144)

        self.world = World(
            self.engine.sound_engine,
            self.engine.texture_manager,
            self.engine.window,
            7,
            level_file="level0.lvl"
        )

        print_debug(f"Loaded {self.world.texture_manager.count_textures()} surfaces into memory!")

    def run(self):
        self.engine.run(self.world)
