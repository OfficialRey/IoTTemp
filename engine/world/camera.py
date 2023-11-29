from engine.core.vector import Vector
from engine.core.window import Window
from engine.props.types.movable import Movable
from engine.props.types.sprite import Sprite

VISIBLE_OFFSET = 16


class Camera(Movable):

    def __init__(self, window: Window, zoom: float = 1):
        super().__init__()
        self.position = Vector()
        self._zoom = zoom
        self.window = window
        self.resolution = self.window.resolution

    def set_zoom(self, zoom: float):
        self._zoom = zoom

    def get_zoom(self):
        return self._zoom

    def is_visible(self, sprite: Sprite) -> bool:
        position = self.get_relative_position(sprite)
        return VISIBLE_OFFSET <= position.x <= self.resolution.x + VISIBLE_OFFSET and \
            VISIBLE_OFFSET <= position.y <= self.resolution.y + VISIBLE_OFFSET

    def get_relative_position(self, movable: Movable) -> Vector:
        return movable.position - self.position

    def get_center_position(self):
        return self.position + self.resolution / 2
