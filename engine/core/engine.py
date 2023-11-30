from enum import Enum

import pygame

from engine.core.communication import Communication
from engine.core.vector import Vector
from engine.core.input_manager import InputManager
from engine.core.window import Window
from protocol.server_package import ServerPackage
from sound.arduino_sound_list import ArduinoSoundData

MILLI_SECONDS = 1000


class RunMode(Enum):
    COMPUTER = ()
    WEAPON = ()


class Engine:

    def __init__(self, communication: Communication, window_resolution: Vector = Vector(1920, 1080), max_fps: int = 60,
                 run_mode: RunMode = RunMode.COMPUTER):
        self.window = Window(window_resolution)
        self.input_manager = InputManager()
        self.communication = communication
        self.inputs = self.input_manager.read()
        self.done = False
        self.run_mode = run_mode

        self.clock = pygame.time.Clock()
        self.max_fps = max_fps
        self.target_delta_time = 1 / self.max_fps
        self.delta_time = self.target_delta_time

        pygame.mouse.set_visible(False)

    def run(self, world) -> None:
        while not self.done:
            self._create_package()
            self._check_events()

            world.process(self.input_manager, self.delta_time)
            world.render(self.window)

            self._update_package(world)
            self.communication.run(self.package)
            self._update_delta_time()

    def _update_delta_time(self) -> None:
        self.delta_time = self.clock.tick(self.max_fps) / MILLI_SECONDS

    def _create_package(self):
        self.package = ServerPackage()

    def _update_package(self, world):
        if world.player_shot:
            self.package.sound_number = ArduinoSoundData.EXAMPLE.value

    def _check_events(self) -> None:
        for event in pygame.event.get():
            self.window.update(event)
            self.input_manager.update(event)

        # Update Input
        self.inputs = self.input_manager.read()
