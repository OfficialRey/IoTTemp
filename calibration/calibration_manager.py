from typing import List

from calibration.calibration_point import CalibrationPoint


class CalibrationManager:

    def __init__(self):
        self.calculation_points: List[CalibrationPoint] = []

    # Use last 3 - 5 values and calculate median
    # Ignore values that are way too high

    def add_calculation_point(self, point):
        self.calculation_points.append(point)

    def calculate_formula(self):
        # TODO: Use points to calculate formula required variables
        pass

    def get_plane_position(self, yaw: float, pitch: float):
        # TODO: Add formula
        return yaw, pitch
