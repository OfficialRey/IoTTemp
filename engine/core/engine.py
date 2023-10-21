from enum import Enum

import pygame

from engine.core.vector import Vector
from engine.util.constants import BLACK
from engine.world.world import World
from engine.core.input_manager import InputManager
from engine.core.window import Window

MILLI_SECONDS = 1000


class RunMode(Enum):
    COMPUTER = ()
    WEAPON = ()


class Engine:

    def __init__(self, window_resolution: Vector = Vector(1920, 1080), max_fps: int = 60,
                 run_mode: RunMode = RunMode.COMPUTER):
        self.window = Window(window_resolution)
        self.input_manager = InputManager()
        self.inputs = self.input_manager.read()
        self.done = False
        self.run_mode = run_mode

        self.clock = pygame.time.Clock()
        self.max_fps = max_fps
        self.target_delta_time = 1 / self.max_fps
        self.delta_time = self.target_delta_time

    def run(self, world: World) -> None:
        while not self.done:
            self._check_events()
            self.process(world)
            self.render(world)
            self._update_delta_time()

    def _update_delta_time(self) -> None:
        self.delta_time = self.clock.tick(self.max_fps) / MILLI_SECONDS

    def _check_events(self) -> None:
        for event in pygame.event.get():
            self.window.update(event)
            self.input_manager.update(event)

        # Update Input
        self.inputs = self.input_manager.read()

    def process(self, world: World):
        self._process_player(world)
        self._process_units(world)

    def _process_player(self, world: World):
        world.cursor.update(self.delta_time)
        world.cursor.position = Vector(self.input_manager.mouse_x, self.input_manager.mouse_y)

    def _process_units(self, world: World):
        for enemy in world.enemies:
            enemy.update_relative_position(world.camera)

    def render(self, world: World) -> None:
        self.window.fill(BLACK)
        self._render_level(world)
        self._render_units(world)
        self._render_cursor(world)
        pygame.display.flip()

    def _render_level(self, world: World) -> None:
        zoom = world.get_camera_zoom()
        camera_x = int(world.camera.position.x)
        camera_y = int(world.camera.position.y)

        sprite_width, sprite_height = world.level_data.texture_atlas.get_texture_size()

        for x in range(int(-sprite_width), int(world.camera.resolution.x * zoom + sprite_width * 2), sprite_width):
            for y in range(int(-sprite_height), int(world.camera.resolution.y * zoom + sprite_height * 2),
                           sprite_height):
                x_pos = (x + camera_x) // sprite_width
                y_pos = (y + camera_y) // sprite_height
                if 0 <= x_pos < world.level_data.width and 0 <= y_pos < world.level_data.height:
                    self.window.surface.blit(world.level_data.get_texture(x_pos, y_pos).image,
                                             (x - camera_x % sprite_width, y - camera_y % sprite_height))

    def _render_units(self, world: World) -> None:
        camera = world.camera
        for unit in world.units:
            if camera.is_visible(unit):
                unit.render(self.window.surface, camera.get_relative_position(unit))

    def _render_cursor(self, world: World) -> None:
        self.window.surface.blit(world.cursor.get_texture().image, world.cursor.position.as_tuple())