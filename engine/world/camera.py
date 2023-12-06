from engine.core.vector import Vector
from engine.core.window import Window
from engine.props.types.movable import Movable
from engine.props.types.sprite import Sprite
from engine.world.level_data import LevelData

VISIBLE_OFFSET = 128


class Camera(Movable):

    def __init__(self, window: Window, zoom: float = 1):
        super().__init__()
        self._zoom = zoom
        self.window = window
        self.resolution = self.window.resolution

    def set_zoom(self, zoom: float):
        self._zoom = zoom

    def get_zoom(self):
        return self._zoom

    def is_visible(self, sprite: Sprite) -> bool:
        position = self.get_relative_position(sprite)
        return -VISIBLE_OFFSET <= position.x <= self.resolution.x + VISIBLE_OFFSET and \
               -VISIBLE_OFFSET <= position.y <= self.resolution.y + VISIBLE_OFFSET

    def get_position(self):
        return self.center_position - self.resolution / 2

    def get_relative_position(self, movable: Movable) -> Vector:
        return movable.center_position - self.get_position()

    def clamp_position(self, level_data: LevelData, position: Vector) -> Vector:
        position.x = max(self.resolution.x / 2, position.x)
        position.y = max(self.resolution.y / 2, position.y)
        position.x = min(level_data.width * level_data.texture_atlas.get_texture_width() - self.resolution.x / 2,
                         position.x)
        position.y = min(level_data.height * level_data.texture_atlas.get_texture_height() - self.resolution.y / 2,
                         position.y)
        return position

    def set_position_smooth(self, level_data: LevelData, position: Vector, speed: float = 0.6):
        position_to_target = (position - self.center_position) / 10
        target_position = self.center_position + position_to_target * speed
        self.center_position = self.clamp_position(level_data, target_position)
