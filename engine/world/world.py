import pygame.sprite

from engine.core.vector import Vector
from engine.core.window import Window
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.enemy.storage.centipede.centipede import Centipede
from engine.props.player.cursor import Cursor
from engine.props.player.player import Player
from engine.world.camera import Camera
from engine.world.level_data import LevelData


class World:

    def __init__(self, texture_manager: TextureManager, level_data: LevelData, window: Window, zoom: float):
        self.level_data = level_data
        self.camera = Camera(window, zoom)
        self.player = Player(texture_manager)
        self.texture_atlas = self.level_data.texture_atlas

        self.units = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.units.add(self.enemies)
        self.units.add(self.player)

        # centipede = Centipede(texture_manager)
        #
        # self.enemies.add(centipede)
        # self.units.add(centipede)

        self.set_camera_zoom(zoom)

    # Camera Manipulation
    def get_camera_zoom(self):
        return self.camera.get_zoom()

    def set_camera_zoom(self, zoom: float):
        self.camera.set_zoom(zoom)

        target_width = int(self.texture_atlas.base_width * zoom)
        target_height = int(self.texture_atlas.base_height * zoom)

        self.texture_atlas.set_size(target_width, target_height)

        for unit in self.units.sprites():
            unit.set_size(target_width, target_height)

    def set_camera_position(self, position: Vector):
        if position.x + self.camera.resolution.x > self.level_data.width * self.texture_atlas.sprite_width:
            position.x = self.level_data.width * self.texture_atlas.sprite_width - self.camera.resolution.x
        if position.y + self.camera.resolution.y > self.level_data.height * self.texture_atlas.sprite_height:
            position.y = self.level_data.height * self.texture_atlas.sprite_height - self.camera.resolution.y
        if position.x < 0:
            position.x = 0
        if position.y < 0:
            position.y = 0
        self.camera.position = position
