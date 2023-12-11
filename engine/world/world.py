import os

import pygame.sprite

from engine.core.vector import Vector
from engine.core.window import Window
from engine.game_info.game_info import GameInformation
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.bullet.bullet import BulletManager
from engine.props.data import UnitData
from engine.props.player.player import Player
from engine.props.types.unit import ShootingUnit, Unit
from engine.props.weapon.weapon import WeaponManager
from engine.sound.game_sound import SoundEngine
from engine.util.constants import WHITE
from engine.util.debug import print_debug
from engine.util.resources import get_resource_path
from engine.world.camera import Camera
from engine.world.level_data import LevelData, load_level
from game.wave_manager import WaveManager


class World:

    def __init__(self, sound_engine: SoundEngine, texture_manager: TextureManager, window: Window, zoom: float,
                 level_file: str = None):
        print_debug("Creating world...")

        self.texture_manager = texture_manager
        self.bullet_manager = BulletManager(self.texture_manager.bullets)
        self.weapon_manager = WeaponManager(self.bullet_manager)
        self.sound_engine = sound_engine
        self.camera = Camera(window, zoom)

        if level_file is None:
            self.level_data = LevelData(self.texture_manager.level_textures, "Test", 20, 20)
        else:
            path = self.path = os.path.join(get_resource_path(), os.path.join("level", level_file))
            self.level_data = load_level(path)
        self.player = Player(self.sound_engine, self.texture_manager, self.weapon_manager, UnitData.PLAYER)
        self.texture_atlas = self.level_data.texture_atlas

        self.units = pygame.sprite.Group()
        self.units.add(self.player)

        # Server Package Values
        self.player_shot = False
        self.player_damaged = False
        self.enemy_killed = False
        self.set_camera_zoom(zoom)

        self.wave_manager = WaveManager(self, self.bullet_manager)

    def get_camera_zoom(self):
        return self.camera.get_zoom()

    def set_camera_zoom(self, zoom: float):
        self.camera.set_zoom(zoom)

        # Update every single animation atlas to adjust to zoom
        for texture_atlas in self.texture_manager.game_textures:
            texture_atlas.scale_textures(Vector(zoom, zoom))

    def set_camera_position(self, position: Vector):
        position.x = max(self.camera.resolution.x / 2,
                         min(self.level_data.width * self.texture_atlas.get_texture_width() - self.camera.resolution.x / 2,
                             position.x))

        if position.x + self.camera.resolution.x > self.level_data.width * self.texture_atlas.sprite_width:
            position.x = self.level_data.width * self.texture_atlas.sprite_width - self.camera.resolution.x
        if position.y + self.camera.resolution.y > self.level_data.height * self.texture_atlas.sprite_height:
            position.y = self.level_data.height * self.texture_atlas.sprite_height - self.camera.resolution.y

        # Clamp values
        if position.x < 0:
            position.x = 0
        if position.y < 0:
            position.y = 0
        self.camera.position = position

    def process(self, game_info: GameInformation, delta_time: float):
        self.wave_manager.run(delta_time)
        self._reset_package_values()
        self._process_player(game_info, delta_time)
        self._process_units(delta_time)
        self._process_bullets()
        self._remove_units()

    def _reset_package_values(self):
        self.player_shot = False
        self.player_damaged = False
        self.enemy_killed = False

    def _process_player(self, game_info: GameInformation, delta_time: float):
        self.player.handle_input(game_info, self.camera, delta_time)

        # Player just shot
        if self.player.current_shot_timer == 0:
            self.player_shot = True

        # Update Camera
        player_to_cursor = (self.player.cursor.center_position - self.camera.get_relative_position(
            self.player)) / 4

        position = (self.player.center_position + player_to_cursor)
        self.camera.set_position_smooth(self.level_data, position)

    def _process_units(self, delta_time: float):
        for unit in self.units.sprites():
            unit.update(self, delta_time)

    def _process_bullets(self):
        for unit in self.units.sprites():
            if isinstance(unit, ShootingUnit):
                bullets = unit.get_bullets()

                if len(bullets) == 0:
                    continue

                for target in self.units.sprites():
                    # Return if trying to attack own team
                    if unit.is_enemy == target.is_enemy:
                        continue
                    target.register_bullet_hits(bullets)

    def _remove_units(self):
        to_remove = []
        for unit in self.units.sprites():
            if unit.can_remove():
                to_remove.append(unit)

        self.units.remove(*to_remove)

    def render(self, window: Window):
        window.fill(WHITE)
        self._render_level(window)
        self._render_units(window)
        self.wave_manager.render(window)
        pygame.display.flip()

    def _render_level(self, window: Window) -> None:
        zoom = self.get_camera_zoom()
        camera_x, camera_y = self.camera.get_position().as_int().as_tuple()

        sprite_width, sprite_height = self.level_data.texture_atlas.get_texture_size()

        for layer in range(self.level_data.layers):
            for x in range(int(-sprite_width), int(self.camera.resolution.x * zoom + sprite_width * 2), sprite_width):
                for y in range(int(-sprite_height), int(self.camera.resolution.y * zoom + sprite_height * 2),
                               sprite_height):
                    x_pos = (x + camera_x) // sprite_width
                    y_pos = (y + camera_y) // sprite_height
                    if 0 <= x_pos < self.level_data.width and 0 <= y_pos < self.level_data.height:
                        texture = self.level_data.get_texture(x_pos, y_pos, layer)
                        if texture is not None:
                            window.surface.blit(texture.get_image(),
                                                (x - camera_x % sprite_width, y - camera_y % sprite_height))

    def _render_units(self, window: Window) -> None:
        for unit in self.units:
            if unit is not self.player:
                unit.render(window.surface, self.camera)
        self.player.render(window.surface, self.camera)

    def are_enemies_dead(self):
        for unit in self.units.sprites():
            if not isinstance(unit, Unit):
                continue
            if isinstance(unit, Player):
                continue
            if unit.is_dead():
                continue
            return False
        return True
