import struct
from typing import List

from protocol.game_package import GamePackage

LEDS = "leds"
RUMBLE = "rumble"
LASER = "laser"

LED_LENGTH = 15


class ServerPackage(GamePackage):
    leds: List[bool]
    rumble: bool
    laser: bool

    def __init__(self, leds: List[bool] = None, rumble: bool = False, laser: bool = False, sound_number: int = -1):
        if leds is None:
            leds = [False] * LED_LENGTH
        # Position:
        # Format: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.leds = leds
        self.laser = laser
        self.rumble = rumble
        self.sound_number = sound_number
        self.package = self.construct()

    def construct(self) -> bytes:
        return struct.pack('<??i15?', self.laser, self.rumble, self.sound_number, *self.leds)

    def __str__(self):
        return f"Server Package: LED:{self.leds} | Laser: {self.laser} | Rumble: {self.rumble}" \
               f" | Sound: {self.sound_number}"
