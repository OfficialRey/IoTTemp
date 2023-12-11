from enum import Enum

import pygame

from calibration.calibration_manager import CalibrationManager
from engine.core.communication import Communication
from engine.core.vector import Vector
from engine.core.window import Window
from engine.game_info.game_info import GameInformation
from engine.graphics.textures.texture_manager import TextureManager
from engine.menu.menu import Menu
from engine.menu.storage.calibration_menu import CalibrationMenu
from engine.sound.game_sound import SoundEngine
from engine.util.debug import print_debug
from protocol.server_package import ServerPackage
from protocol.weapon_package import WeaponPackage

MILLI_SECONDS = 1000

UDP_IP = "192.168.2.45"
RECEIVER_IP = "0.0.0.0"

UDP_PORT = 8888
RECEIVER_PORT = 5050

RECEIVER_BUFFER_SIZE = 0


class RunMode(Enum):
    COMPUTER = ()
    WEAPON = ()


class Engine:

    def __init__(self, window_resolution: Vector = Vector(1920, 1080), max_fps: int = 60):
        print_debug("Creating engine...")

        self.window = Window(window_resolution)
        self.communication = Communication(UDP_IP, UDP_PORT, RECEIVER_IP, RECEIVER_PORT, RECEIVER_BUFFER_SIZE, self,
                                           synthesize_connection=True)  # TODO: Remove fake connection when running
        self.calibration_manager = CalibrationManager()
        self.texture_manager = TextureManager()
        # self.input_manager = InputManager() DEPRECATED
        # self.inputs = self.input_manager.read() DEPRECATED
        self.sound_engine = SoundEngine()
        self.done = False

        self.clock = pygame.time.Clock()
        self.max_fps = max_fps
        self.delta_time = 0

        self.game_info = GameInformation()
        self.server_package = ServerPackage()
        self.weapon_package = WeaponPackage()

        self.current_menu: Menu = CalibrationMenu(self)
        self.pygame_events = []

    def run(self, world) -> None:
        # Reset clock and set delta time to 0 to not use loading time as calculation time
        self.clock.tick(self.max_fps)
        self.delta_time = 0
        print_debug("Starting main loop...")
        while not self.done:

            self._check_events()
            self._communicate()
            self._update_game_info()

            if self.current_menu is not None:
                self.current_menu.render(self.window)
                self.current_menu.run(self.game_info)

                # Fix clock working improperly
                self.clock.tick(self.max_fps)
                self.delta_time = 0
                continue

            world.process(self.game_info, self.delta_time)
            world.render(self.window)

            self._update_delta_time()

    def _update_delta_time(self) -> None:
        self.delta_time = self.clock.tick(self.max_fps) / MILLI_SECONDS
        print(f"FPS: {1 / self.delta_time}")

    def _update_game_info(self):
        self.game_info.update(self.weapon_package)

        # Update X and Y of GameInformation
        self.game_info.x, self.game_info.y = self.calibration_manager.get_plane_position(self.game_info.yaw,
                                                                                         self.game_info.pitch)

    def _check_events(self) -> None:
        self.pygame_events = pygame.event.get()
        for event in self.pygame_events:
            self.window.update(event)
            # self.input_manager.update(event) DEPRECATED

        # Update Input
        # self.inputs = self.input_manager.read() DEPRECATED

    def _communicate(self):
        # Update Server Package
        self.server_package.laser = isinstance(self.current_menu, CalibrationMenu)

        self.weapon_package = self.communication.run(self.server_package)
