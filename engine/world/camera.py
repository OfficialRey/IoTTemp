from engine.core.vector import Vector
from engine.core.window import Window
from engine.props.types.movable import Movable
from engine.props.types.sprite import Sprite


class Camera(Movable):

    def __init__(self, window: Window, zoom: float = 1):
        super().__init__()
        self.position = Vector()
        self._zoom = zoom
        self.window = window
        self.resolution = Vector(window.resolution.x // zoom, window.resolution.y // zoom)

    def set_zoom(self, zoom: float):
        self._zoom = zoom
        self.resolution = self.window.resolution

    def get_zoom(self):
        return self._zoom

    def is_visible(self, sprite: Sprite) -> bool:
        position = self.get_relative_position(sprite)
        return 0 <= position.x <= self.resolution.x and 0 <= position.y <= self.resolution.y

    def get_relative_position(self, movable: Movable) -> Vector:
        return movable.position - self.position

    def get_center_position(self):
        return self.position + self.resolution / 2