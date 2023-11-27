from typing import List

from protocol.game_package import GamePackage

LEDS = "leds"
RUMBLE = "rumble"
LASER = "laser"


class ServerPackage(GamePackage):
    leds: List
    rumble: bool
    laser: bool
    package: dict

    # TODO: Play sounds

    def __init__(self, leds: List[int] = None, rumble: bool = False, laser: bool = False, json: dict = None):
        if json is None:
            if leds is None:
                leds = []
            self.leds = leds
            self.rumble = rumble
            self.laser = laser
            self.package = self.construct()
        else:
            self.package = self.deconstruct(json)

    def construct(self):
        return {
            LEDS: self.leds,
            RUMBLE: self.rumble,
            LASER: self.laser
        }

    def deconstruct(self, json: dict):
        if LEDS in json:
            self.leds = json[LEDS]
        if RUMBLE in json:
            self.rumble = json[RUMBLE]
        if LASER in json:
            self.laser = json[LASER]
        return json
