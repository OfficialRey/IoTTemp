class CalibrationPoint:

    def __init__(self, x: int, y: int, yaw: float, pitch: float):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.pitch = pitch

    def __str__(self):
        return f"X: {self.x}, Y: {self.y} | Yaw: {self.yaw}, Pitch: {self.pitch}"
