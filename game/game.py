from engine.core.communication import Communication
from engine.core.engine import Engine
from engine.graphics.textures.texture_manager import TextureManager
from engine.world.level_data import LevelData
from engine.world.world import World

UDP_IP = "192.168.2.45"
RECEIVER_IP = "0.0.0.0"

UDP_PORT = 8888
RECEIVER_PORT = 5050

RECEIVER_BUFFER_SIZE = 0


class TopDownGame:

    def __init__(self):
        self.communication = Communication(UDP_IP, UDP_PORT, RECEIVER_IP, RECEIVER_PORT, RECEIVER_BUFFER_SIZE)
        self.engine = Engine(self.communication, max_fps=90)
        self.texture_manager = TextureManager()
        self.world = World(
            self.texture_manager,
            LevelData(self.texture_manager.level_textures, "Test", 512, 512),
            self.engine.window,
            7
        )

    def run(self):
        self.engine.run(self.world)
