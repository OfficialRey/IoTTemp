from typing import List

import pygame.draw
from pygame.math import clamp

from engine.core.vector import Vector
from engine.core.window import Window
from engine.editor.editor_widget import LevelEditorSelectTextureButton, LevelEditorScrollTextureButton
from engine.graphics.gui.widget import Button
from engine.graphics.textures.atlas import LevelAtlas
from engine.graphics.textures.texture_animation import AnimationType
from engine.graphics.textures.texture_manager import TextureManager
from engine.util.constants import RED, WHITE, BLACK
from engine.world.level_data import LevelData

from tkinter import Tk
from tkinter.filedialog import askopenfilename

from engine.world.world import World

DRAW_PERCENTAGE = 0.8
BOX_OFFSET = 5
GRAPHICS_PER_ROW = 20


# TODO: Multiple layers per level
# TODO: Change layers in editor
# TODO: Save level layouts
# TODO: Level Collision editor
# TODO: Delete textures

class LevelEditor:
    texture_atlas: LevelAtlas
    level_data: LevelData
    buttons: List[Button]
    scroll_buttons: List[LevelEditorScrollTextureButton]

    def __init__(self, fps: int = 60):
        self.window = Window(Vector(1920, 1080), full_screen=False)

        # Editor Parameters
        self.done = False
        self.texture_manager = TextureManager()
        self.texture_atlas = self.texture_manager.level_textures
        self.level_data = None
        self.world = None

        self.selected_texture = 0
        self.current_row = 0

        self.upper_bound = 0

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.position = Vector(0, 0)
        self.n_textures_x = 0
        self.n_textures_y = 0

    def select_textures(self):
        while self.texture_atlas is None:
            Tk().withdraw()
            file = askopenfilename().replace("\\", "/")
            file_name = file.split("/")[-1]
            path = "".join([(file.split("/")[index] + "/") for index in range(len(file.split("/")) - 1)])
            sprite_width = int(input("Sprite Width:"))
            sprite_height = int(input("Sprite Height:"))
            self.texture_atlas = LevelAtlas(path, file_name, sprite_width, sprite_height)

    def create_world(self):
        # world_name = input("World Name:")
        # width = int(input("Width:"))
        # height = int(input("Height:"))
        world_name = "Test"
        width = 200
        height = 200
        self.level_data = LevelData(self.texture_atlas, world_name, width, height)
        self.world = World(self.texture_manager, self.level_data, self.window, 5)
        self.n_textures_x = self.window.get_width() // self.texture_atlas.sprite_width
        self.n_textures_y = self.window.get_height() // self.texture_atlas.sprite_height

    def load_textures(self):
        self.buttons = []
        for index in range(len(self.texture_atlas.textures)):
            button = LevelEditorSelectTextureButton(self, texture_id=index)
            button.enabled = False
            button.set_content(self.texture_atlas.textures[index].base_image)
            self.buttons.append(button)

        self.upper_bound = len(self.buttons) // GRAPHICS_PER_ROW

        # Scroll Buttons
        self.scroll_buttons = []

        button = LevelEditorScrollTextureButton(self, -1)
        button.enabled = True
        button.set_content(self.texture_manager.arrow_up.get_texture(AnimationType.GENERIC).image)
        button.set_area((self.window.get_width() * 0.95, self.window.get_height() * 0.81,
                         self.texture_manager.arrow_up.sprite_width * 5,
                         self.texture_manager.arrow_up.sprite_height * 5))
        self.scroll_buttons.append(button)

        button = LevelEditorScrollTextureButton(self, 1)
        button.enabled = True
        button.set_content(self.texture_manager.arrow_down.get_texture(AnimationType.GENERIC).image)
        button.set_area((self.window.get_width() * 0.95, self.window.get_height() * 0.9,
                         self.texture_manager.arrow_up.sprite_width * 5,
                         self.texture_manager.arrow_up.sprite_height * 5))
        self.scroll_buttons.append(button)

    def update_gui(self):
        for button in self.buttons:
            button.enabled = False

        for i in range(GRAPHICS_PER_ROW * 2):
            index = self.current_row * GRAPHICS_PER_ROW + i
            if index >= len(self.buttons):
                return
            button = self.buttons[index]
            button.set_area((BOX_OFFSET * 2 + (i % GRAPHICS_PER_ROW) * self.texture_atlas.sprite_width * 1.1,
                             self.window.get_height() * DRAW_PERCENTAGE + BOX_OFFSET * 3 + (
                                     i // GRAPHICS_PER_ROW) * self.texture_atlas.sprite_height * 1.2,
                             self.texture_atlas.sprite_width,
                             self.texture_atlas.sprite_height))
            button.enabled = True

    def run(self):
        self.select_textures()
        self.create_world()
        self.load_textures()
        self.update_gui()

        while not self.done:
            self.clock.tick(self.fps)
            self.check_events()
            self.render()

    def check_events(self):
        for event in pygame.event.get():
            for button in self.buttons:
                button.act(event)
            for button in self.scroll_buttons:
                button.act(event)
            if event.type == pygame.QUIT:
                exit()

        # Movement
        keys = pygame.key.get_pressed()
        x = keys[pygame.K_d] - keys[pygame.K_a]
        y = keys[pygame.K_s] - keys[pygame.K_w]
        self.position += Vector(x / 2, y / 2)
        self.position.x = clamp(self.position.x, 0, self.level_data.width - self.n_textures_x)
        self.position.y = clamp(self.position.y, 0, self.level_data.height - self.n_textures_y)

        # Mouse
        left_click, _, _ = pygame.mouse.get_pressed()
        if left_click:
            self.draw_level(Vector(*pygame.mouse.get_pos()))

    def render(self):
        self.window.surface.fill(BLACK)
        self.render_world()
        self.render_grid()
        self.render_gui()
        pygame.display.flip()

    def render_world(self):
        for x in range(self.n_textures_x):
            for y in range(self.n_textures_y):
                texture_id = self.level_data.get_texture_id(x + int(self.position.x), y + int(self.position.y))
                if texture_id < 0:
                    continue

                texture = self.texture_atlas[texture_id]
                destination = (
                    x * self.texture_atlas.sprite_width,
                    y * self.texture_atlas.sprite_height)
                self.window.surface.blit(texture.image, destination)

    def render_grid(self):
        width = self.window.get_width()
        height = self.window.get_height()
        for x in range(0, width, self.texture_atlas.sprite_width):
            pygame.draw.line(self.window.surface, RED, (x, 0), (x, height))

        for y in range(0, height, self.texture_atlas.sprite_height):
            pygame.draw.line(self.window.surface, RED, (0, y), (width, y))

    def render_gui(self):
        # Render Overlay
        pygame.draw.rect(self.window.surface, BLACK, (
            0, self.window.get_height() * DRAW_PERCENTAGE, self.window.get_width(), self.window.get_height()))
        pygame.draw.rect(self.window.surface, WHITE, (
            BOX_OFFSET,
            self.window.get_height() * DRAW_PERCENTAGE + BOX_OFFSET,
            self.window.get_width() - 2 * BOX_OFFSET,
            self.window.get_height()))

        # Render Textures
        self.render_gui_textures()

    def render_gui_textures(self):
        for button in self.buttons:
            button.render(self.window.surface)
        for button in self.scroll_buttons:
            button.render(self.window.surface)

    def select_texture(self, texture_id: int):
        self.buttons[self.selected_texture].background_color = None
        self.selected_texture = texture_id
        self.buttons[self.selected_texture].background_color = BLACK

    def scroll_texture(self, direction: int):
        self.current_row += direction
        self.current_row = self.upper_bound if self.current_row >= self.upper_bound else self.current_row
        self.current_row = 0 if self.current_row < 0 else self.current_row
        self.update_gui()

    def draw_level(self, position: Vector):
        # Get Level coordinates
        if position.y >= self.window.get_height() * DRAW_PERCENTAGE:
            return
        x = position.x // self.texture_atlas.sprite_width + self.position.x
        y = position.y // self.texture_atlas.sprite_height + self.position.y
        self.level_data.place_texture(self.selected_texture, int(x), int(y))
