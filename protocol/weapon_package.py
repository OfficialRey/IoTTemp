from protocol.game_package import GamePackage

PITCH = "pitch"
YAW = "yaw"
FIRE = "fire"
ABILITY = "ability"
CALIBRATION = "calibration"


class WeaponPackage(GamePackage):
    yaw: float
    pitch: float
    fire_trigger: bool
    ability_trigger: bool
    calibration_trigger: bool
    package: dict

    def __init__(self, yaw: float = 0, pitch: float = 0, fire_trigger: bool = False, ability_trigger: bool = False,
                 calibration_trigger: bool = False):
        self.yaw = yaw
        self.pitch = pitch
        self.fire_trigger = fire_trigger
        self.ability_trigger = ability_trigger
        self.calibration_trigger = calibration_trigger
