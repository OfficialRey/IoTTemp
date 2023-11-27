from protocol.game_package import GamePackage

PITCH = "pitch"
YAW = "yaw"
FIRE = "fire"
ABILITY = "ability"
CALIBRATION = "calibration"


class WeaponPackage(GamePackage):
    pitch: float
    yaw: float
    fire_trigger: bool
    ability_trigger: bool
    calibration_trigger: bool
    package: dict

    def __init__(self, pitch: float, yaw: float, fire_trigger: bool, ability_trigger: bool, calibration_trigger: bool,
                 json: dict = None):
        if json is None:
            self.pitch = pitch
            self.yaw = yaw
            self.fire_trigger = fire_trigger
            self.ability_trigger = ability_trigger
            self.calibration_trigger = calibration_trigger
            self.package = self.construct()
        else:
            self.package = self.deconstruct(json)

    def construct(self):
        return {
            PITCH: self.pitch,
            YAW: self.yaw,
            FIRE: self.fire_trigger,
            ABILITY: self.ability_trigger,
            CALIBRATION: self.calibration_trigger
        }

    def deconstruct(self, json: dict):
        if PITCH in json:
            self.pitch = json[PITCH]
        if YAW in json:
            self.yaw = json[YAW]
        if FIRE in json:
            self.fire_trigger = json[FIRE]
        if ABILITY in json:
            self.ability_trigger = json[ABILITY]
        if CALIBRATION in json:
            self.calibration_trigger = json[CALIBRATION]
        return json
