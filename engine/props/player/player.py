from engine.graphics.textures.texture_manager import TextureManager
from engine.props.entity import Entity


class Player(Entity):

    def __init__(self, texture_manager: TextureManager):
        super().__init__(texture_manager.player, 100, 20, 20)
