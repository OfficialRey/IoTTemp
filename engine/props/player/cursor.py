from engine.core.vector import Vector
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.entity import Sprite


class Cursor(Sprite):

    def __init__(self, texture_manager: TextureManager):
        super().__init__(texture_manager.cursor)
        self.position = Vector()

    def set_position(self, position: Vector):
        self.position = position
