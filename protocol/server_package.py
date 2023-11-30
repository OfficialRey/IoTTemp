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

    def __init__(self, leds: List[bool] = None, rumble: bool = False, laser: bool = False, sound_number: int = -1,
                 json: dict = None):
        if json is None:
            if leds is None:
                leds = [False] * LED_LENGTH
            # Position:
            # Format: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.leds = leds
            self.rumble = rumble
            self.laser = laser
            self.sound_number = sound_number
            self.package = self.construct()
        else:
            self.package = self.deconstruct(json)

    def construct(self) -> bytes:
        return struct.pack('<??i15?', self.laser, self.rumble, self.sound_number, *self.leds)

    def deconstruct(self, json: dict) -> bytes:
        if LEDS in json:
            self.leds = json[LEDS]
        if RUMBLE in json:
            self.rumble = json[RUMBLE]
        if LASER in json:
            self.laser = json[LASER]
        return self.construct()
