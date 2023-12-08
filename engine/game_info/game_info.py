from statistics import median

from protocol.weapon_package import WeaponPackage

BUTTONS = [M1, M2, M3] = [0, 1, 2]


class TriggerInput:

    def __init__(self, pressed: bool = False, held: bool = False, released: bool = False):
        self.pressed = pressed  # Trigger is active for one frame
        self.held = held  # Trigger is active for several frames
        self.released = released  # Trigger is inactive for one frame

    def update(self, trigger_value: bool):
        if trigger_value:  # Trigger is currently active
            self.released = False
            if not self.pressed and not self.held:  # Trigger was not previously active
                self.pressed = True
                self.held = True
                self.released = False
            elif self.held:  # Trigger was previously active
                self.pressed = False
        elif not trigger_value:  # Trigger is currently inactive
            if self.pressed or self.held:  # Trigger was previously active
                self.released = True
            else:
                self.released = False
            self.pressed = False
            self.held = False

    def __str__(self):
        return f"Trigger( Pressed: {self.pressed} | Hold: {self.held} | Released: {self.released} )"


class GameInformation:

    def __init__(self, x: int = 0, y: int = 0, yaw: float = 0, pitch: float = 0, median_length: int = 10):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.pitch = pitch
        self.yaws = [yaw for _ in range(median_length)]
        self.pitchs = [pitch for _ in range(median_length)]
        self.fire_trigger = TriggerInput()

        self.update_count = 0

    def update(self, weapon_package: WeaponPackage):
        self.fire_trigger.update(weapon_package.fire_trigger)
        self.update_count += 1

        self._update_median(weapon_package)

    def _update_median(self, weapon_package: WeaponPackage):
        self.yaws.append(weapon_package.yaw)
        self.pitchs.append(weapon_package.pitch)

        self.yaws.pop(0)
        self.pitchs.pop(0)

        self.yaw = median(self.yaws)
        self.pitch = median(self.pitchs)


if __name__ == '__main__':
    # Trigger Test
    trigger = TriggerInput()
    print(trigger)
    trigger.update(True)  # Activating trigger
    print(trigger)
    trigger.update(True)  # Holding trigger
    print(trigger)
    trigger.update(False)  # Releasing trigger
    print(trigger)
    trigger.update(False)  # Inactive trigger
    print(trigger)

    # -> Works like a charm
