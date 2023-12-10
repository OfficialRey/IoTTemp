# TODO: Add Enemy Spawn-points
import os
from typing import Tuple, List

from random import random, choice

import pygame.font

from engine.core.vector import Vector
from engine.core.window import Window
from engine.props.enemy.storage.centipede.centipede import Centipede
from engine.props.enemy.storage.spider.spider import ShootingSpider
from engine.util.constants import WHITE
from engine.util.resources import get_resource_path

MAX_WAVE = 1000
SECONDS_PER_SPAWN = 3


class WaveManager:

    def __init__(self, world, bullet_manager, max_units: int = 7, title_detail: int = 50, title_size: int = 100,
                 color: Tuple[int, int, int] = WHITE, title_fade_time: float = 1, title_sustain_time: float = 2,
                 spawn_positions: List[Vector] = None):
        if spawn_positions is None:
            spawn_positions = [Vector()]

        self.world = world
        self.bullet_manager = bullet_manager

        # Wave System
        self.current_wave = 0
        self.enemies = []
        self.spawn_positions = spawn_positions
        self.max_units = max_units

        # Cached title animation
        self.titles = []  # Create a list of lists of cached titles
        self.title_detail = title_detail
        self.title_size = title_size
        self.title_fade_time = title_fade_time
        self.title_sustain_time = title_sustain_time
        self.color = color

        # Title animation
        self.animation_timer = 0

        self._create_render_objects()

    def _create_render_objects(self):
        path = os.path.join(get_resource_path(), os.path.join("font", "ka1.ttf"))
        font = pygame.font.Font(path, self.title_size)
        # Render 999 waves
        for i in range(MAX_WAVE):
            render = font.render(f"Wave {i + 1}", True, self.color)
            current_wave = []
            for j in range(self.title_detail):
                ratio = j / self.title_detail
                stretched_render = pygame.transform.scale(render,
                                                          (render.get_width() * ratio, render.get_height() * ratio))
                current_wave.append(stretched_render)
            self.titles.append(current_wave)

    def run(self, delta_time: float):
        self._spawn_wave(delta_time)
        self.animation_timer += delta_time

    def render(self, window: Window):
        if self.animation_timer > self.title_fade_time + self.title_sustain_time:
            return
        current_titles = self.titles[self.current_wave - 1]

        if self.animation_timer < self.title_fade_time:
            index = self.animation_timer / self.title_fade_time * self.title_detail
        else:
            index = len(current_titles) - 1

        render = current_titles[int(index)]
        position = Vector(
            window.get_width() * 0.5 - render.get_width() * 0.5,
            window.get_height() * 0.2 - render.get_height() * 0.5
        )
        window.surface.blit(render, position.as_tuple())

    def _spawn_wave(self, delta_time: float):
        # Spawn wave if enemies left

        if len(self.enemies) > 0:
            if len(self.world.units) > self.max_units:
                return
            self._spawn_enemy(delta_time)
            return

        if self.world.are_enemies_dead() and len(self.enemies) == 0:
            self._generate_wave()

    def _spawn_enemy(self, delta_time: float):
        spawn_chance = delta_time / SECONDS_PER_SPAWN
        if random() < spawn_chance:
            return
        enemy = self.enemies.pop()
        self.world.units.add(enemy)

    def _generate_wave(self):
        self.enemies = []
        self.current_wave += 1
        self.animation_timer = 0
        level = self.current_wave

        enemy_count = int(3 + (level / 4) + random() * (level / 2))
        for i in range(enemy_count):
            self.enemies.append(self._get_random_enemy(level))

    def _get_random_enemy(self, level: int):
        enemy_type = int(random() * 2)

        spawn_position = choice(self.spawn_positions)

        if enemy_type == 0:
            return Centipede(self.world.sound_engine, self.world.texture_manager, spawn_position, level)
        if enemy_type == 1:
            return ShootingSpider(self.world.sound_engine, self.world.texture_manager, self.bullet_manager.laser,
                                  spawn_position)
