from typing import Tuple, List

from calibration.calibration_point import CalibrationPoint
from engine.core.vector import Vector
from engine.game_info.game_info import GameInformation
from engine.graphics.gui.widget import Label
from engine.menu.menu import Menu

BORDER_DISTANCE = 0.2
BUTTON_SIZE = 50


class CalibrationMenu(Menu):

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.calibration_manager = engine.calibration_manager
        self.count = 0

        self.positions: List[Tuple[int, int]] = [
            (engine.window.get_width() * BORDER_DISTANCE, engine.window.get_height() * BORDER_DISTANCE),
            (engine.window.get_width() * (1 - BORDER_DISTANCE), engine.window.get_height() * BORDER_DISTANCE),
            (engine.window.get_width() * (1 - BORDER_DISTANCE), engine.window.get_height() * (1 - BORDER_DISTANCE))
        ]

        for position in self.positions:
            label = Label((*position, BUTTON_SIZE, BUTTON_SIZE))
            label.set_content(engine.texture_manager.calibrator.textures[0].images[0])
            self.add_widget(label)

        self.update_index()

    def run(self, game_info: GameInformation):
        if game_info.fire_trigger.pressed:
            self.calibration_manager.add_calculation_point(
                CalibrationPoint(*self.widgets[self.count].center_position, game_info.yaw, game_info.pitch))
            self.count += 1
            self.update_index()

    def update_index(self):
        for widget in self.widgets:
            widget.enabled = False

        if len(self.widgets) <= self.count:
            # Done calibrating
            self.engine.current_menu = None
            self.engine.calibration_manager.calculate_formula()
            return

        self.widgets[self.count].enabled = True
