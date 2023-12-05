import pygame.sprite

from engine.core.input_manager import InputManager
from engine.core.vector import Vector
from engine.core.window import Window
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.data import UnitData
from engine.props.enemy.storage.spider.spider import ShootingSpider
from engine.props.player.player import Player
from engine.props.types.unit import ShootingUnit, Unit
from engine.props.weapon.weapon import WeaponManager
from engine.util.constants import WHITE
from engine.util.debug import print_debug
from engine.world.camera import Camera
from engine.world.level_data import LevelData


class World:

    def __init__(self, window: Window, zoom: float):
        print_debug("Creating world...")

        self.texture_manager = TextureManager()
        self.weapon_manager = WeaponManager(self.texture_manager)
        self.camera = Camera(window, zoom)

        self.level_data = LevelData(self.texture_manager.level_textures, "Test", 20, 20)
        self.player = Player(self.texture_manager, self.weapon_manager, UnitData.PLAYER)
        self.texture_atlas = self.level_data.texture_atlas

        self.units = pygame.sprite.Group()
        self.units.add(self.player)

        self.units.add(ShootingSpider(self.texture_manager.spider, self.weapon_manager.laser_gun, Vector()))

        # Server Package Values
        self.player_shot = False
        self.player_damaged = False
        self.enemy_killed = False
        self.set_camera_zoom(zoom)

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

    def process(self, input_manager: InputManager, delta_time: float):
        self._reset_package_values()
        self._process_player(input_manager, delta_time)
        self._process_units(delta_time)
        self._process_bullets()
        self._remove_units()

    def _reset_package_values(self):
        self.player_shot = False
        self.player_damaged = False
        self.enemy_killed = False

    def _process_player(self, input_manager: InputManager, delta_time: float):
        self.player.handle_input(input_manager, self.camera, delta_time)

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
        pygame.display.flip()

    def _render_level(self, window: Window) -> None:
        zoom = self.get_camera_zoom()
        camera_x, camera_y = self.camera.get_position().as_int().as_tuple()

        sprite_width, sprite_height = self.level_data.texture_atlas.get_texture_size()

        for x in range(int(-sprite_width), int(self.camera.resolution.x * zoom + sprite_width * 2), sprite_width):
            for y in range(int(-sprite_height), int(self.camera.resolution.y * zoom + sprite_height * 2),
                           sprite_height):
                x_pos = (x + camera_x) // sprite_width
                y_pos = (y + camera_y) // sprite_height
                if 0 <= x_pos < self.level_data.width and 0 <= y_pos < self.level_data.height:
                    window.surface.blit(self.level_data.get_texture(x_pos, y_pos).get_image(),
                                        (x - camera_x % sprite_width, y - camera_y % sprite_height))

    def _render_units(self, window: Window) -> None:
        for unit in self.units:
            if unit is not self.player:
                unit.render(window.surface, self.camera)
        self.player.render(window.surface, self.camera)
