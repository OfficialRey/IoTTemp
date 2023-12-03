from engine.core.communication import Communication
from engine.core.engine import Engine
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.weapon.weapon import WeaponManager
from engine.util.debug import print_debug
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

        self.world = World(
            self.engine.window,
            7
        )

        print_debug(f"Loaded {self.world.texture_manager.count_textures()} textures into memory...")

    def run(self):
        self.engine.run(self.world)
