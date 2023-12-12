from enum import IntEnum
from typing import List

import pygame.draw
from pygame.math import clamp

from engine.core.vector import Vector
from engine.core.window import Window
from engine.game_info.game_info import GameInformation, TriggerInput
from engine.graphics.atlas.level import LevelAtlas
from engine.graphics.gui.editor.editor_widget import LevelEditorScrollTextureButton, LevelEditorSelectTextureButton
from engine.graphics.gui.widget import Button
from engine.graphics.textures.texture_manager import TextureManager
from engine.util.constants import RED, WHITE, BLACK, GREEN
from engine.util.debug import print_debug
from engine.util.util import sign
from engine.world.collision import CollisionShape
from engine.world.level_data import LevelData, load_level

from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfile

DRAW_PERCENTAGE = 0.8
BOX_OFFSET = 5
GRAPHICS_PER_ROW = 20


# Tutorial:
# Left Click: Place Textures & Select Textures & Change Hitboxes
# MouseWheel: Change Hit-Box Radius
# Right Click: Remove Textures
# Arrow Key Up & Down: Change current layer
# W, A, S, D: Navigate current level layout
# Tabulator: Switch between texture and collision editor
# Ctrl + S: Save current level layout
# Ctrl + L: Load existing level layout


class EditingType(IntEnum):
    TEXTURE = 0,
    COLLISION = 1


class GuiMode(IntEnum):
    HIDE_NONE = 0,
    HIDE_GUI = 1,
    HIDE_ALL = 2,


class LevelEditor:
    texture_atlas: LevelAtlas
    level_data: LevelData
    buttons: List[Button]
    scroll_buttons: List[LevelEditorScrollTextureButton]

    def __init__(self, fps: int = 60):
        self.window = Window(Vector(1920, 1080), full_screen=False)
        pygame.font.init()

        # Editor Parameters
        self.done = False
        self.texture_manager = TextureManager()
        self.texture_atlas = self.texture_manager.level_textures
        self.texture_atlas.scale_textures(Vector(5, 5))
        self.level_data = None

        self.selected_texture = 0
        self.current_layer = 0
        self.current_row = 0

        self.upper_bound = 0

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.position = Vector(0, 0)
        self.n_textures_x = 0
        self.n_textures_y = 0

        self.editing_type = EditingType.TEXTURE
        self.gui_mode = GuiMode.HIDE_NONE
        self.layer_font = pygame.font.SysFont("arial", 20)
        self.layer_info = self.layer_font.render(f"Layer: {self.current_layer}", True, WHITE)

        self.space_trigger = TriggerInput()
        self.tab_trigger = TriggerInput()
        self.left_trigger = TriggerInput()

        self.game_info = GameInformation()

        self.save_path = None

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
        width = int(input("Width:"))
        height = int(input("Height:"))

        self.level_data = LevelData(self.texture_atlas, width, height)
        self.n_textures_x = self.window.get_width() // self.texture_atlas.scaled_width + 1
        self.n_textures_y = self.window.get_height() // self.texture_atlas.scaled_height + 1

    def load_textures(self):
        self.buttons = []
        for index in range(len(self.texture_atlas.textures)):
            button = LevelEditorSelectTextureButton(self, texture_id=index)
            button.enabled = False
            button.set_content(self.texture_atlas.textures[index].images[0])
            self.buttons.append(button)

        self.upper_bound = len(self.buttons) // GRAPHICS_PER_ROW

        # Scroll Buttons
        self.scroll_buttons = []

        button = LevelEditorScrollTextureButton(self, -1)
        button.enabled = True
        button.set_content(self.texture_manager.arrow_up.textures[0].images[0])
        button.set_area((self.window.get_width() * 0.95, self.window.get_height() * 0.81,
                         self.texture_manager.arrow_up.sprite_width * 5,
                         self.texture_manager.arrow_up.sprite_height * 5))
        self.scroll_buttons.append(button)

        button = LevelEditorScrollTextureButton(self, 1)
        button.enabled = True
        button.set_content(self.texture_manager.arrow_down.textures[0].images[0])
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
            start_x = int(BOX_OFFSET * 2 + (i % GRAPHICS_PER_ROW) * self.texture_atlas.scaled_width * 1.1)
            start_y = int(self.window.get_height() * DRAW_PERCENTAGE + BOX_OFFSET * 3 + (
                    i // GRAPHICS_PER_ROW) * self.texture_atlas.sprite_height * self.texture_atlas.sprite_scale.y * 1.2)
            width = int(self.texture_atlas.scaled_width)
            height = int(self.texture_atlas.scaled_height)
            button.set_area((start_x, start_y, width, height))
            button.enabled = True

    def run(self):
        self.select_textures()
        self.create_world()
        self.load_textures()
        self.update_gui()

        while not self.done:
            self.clock.tick(self.fps)
            self.update_game_info()
            self.check_events()
            self.render()

    def check_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if self.gui_mode == GuiMode.HIDE_NONE:
                for button in self.buttons:
                    button.update(self.game_info)
                for button in self.scroll_buttons:
                    button.update(self.game_info)

        # Movement
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        x = keys[pygame.K_d] - keys[pygame.K_a]
        y = int(keys[pygame.K_s] and not keys[pygame.K_LCTRL]) - keys[pygame.K_w]
        layer = keys[pygame.K_UP] - keys[pygame.K_DOWN]

        self.space_trigger.update(keys[pygame.K_SPACE])
        self.tab_trigger.update(keys[pygame.K_TAB])

        self.position += Vector(x, y)
        self.position.x = clamp(self.position.x, 0, max(0, self.level_data.width - self.n_textures_x))
        self.position.y = clamp(self.position.y, 0, max(0, self.level_data.height - self.n_textures_y))

        self.current_layer += layer
        self.current_layer = clamp(self.current_layer, 0, self.level_data.layers - 1)
        if layer != 0:
            self.layer_info = self.layer_font.render(f"Layer: {self.current_layer}", True, WHITE)

        if self.tab_trigger.pressed:
            self.editing_type = int(not self.editing_type)

        self.texture_editing(keys, mouse)
        self.collision_editing(keys, mouse, events)
        self.file_management(keys)

    def texture_editing(self, keys, mouse):
        if self.editing_type == EditingType.TEXTURE:

            # Mouse
            left_click, _, right_click = mouse
            if left_click:
                self.draw_level(Vector(*pygame.mouse.get_pos()))
            if right_click:
                self.remove_level(Vector(*pygame.mouse.get_pos()))

            if self.space_trigger.pressed:
                self.gui_mode += 1
                if self.gui_mode >= len(GuiMode):
                    self.gui_mode = 0

    def collision_editing(self, keys, mouse, events):
        # Collision Switching
        if self.editing_type == EditingType.COLLISION:
            left_click, _, _ = mouse
            self.left_trigger.update(left_click)
            if self.left_trigger.pressed:
                self.change_collision(Vector(*pygame.mouse.get_pos()))
        # Collision Radius
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                y_motion = sign(event.y)
                self.change_collision_radius(Vector(*pygame.mouse.get_pos()), y_motion)

    def file_management(self, keys):
        # Load
        if keys[pygame.K_l] and keys[pygame.K_LCTRL]:
            self.load_level()

        # Save
        if keys[pygame.K_s] and keys[pygame.K_LCTRL]:
            self.save_level()
        if keys[pygame.K_s] and keys[pygame.K_LCTRL] and keys[pygame.K_LSHIFT]:
            self.save_path = None
            self.save_level()

    def render(self):
        self.window.surface.fill(BLACK)

        self.render_world()
        if int(self.editing_type) is int(EditingType.TEXTURE):
            self.render_grid()
            self.render_gui()
        if int(self.editing_type) is int(EditingType.COLLISION):
            self.render_collision()
        pygame.display.flip()

    def render_world(self):
        for layer in range(self.level_data.layers):
            for x in range(min(self.level_data.width, self.n_textures_x)):
                for y in range(min(self.level_data.height, self.n_textures_y)):
                    texture_id = self.level_data.get_texture_id(x + int(self.position.x), y + int(self.position.y),
                                                                layer)
                    if texture_id < 0:
                        continue

                    texture = self.texture_atlas[texture_id]
                    destination = (
                        x * self.texture_atlas.scaled_width,
                        y * self.texture_atlas.scaled_height)
                    self.window.surface.blit(texture.images[0], destination)

    def render_grid(self):
        if self.gui_mode == GuiMode.HIDE_ALL:
            return

        width = self.window.get_width()
        height = self.window.get_height()
        for x in range(0, width, self.texture_atlas.sprite_width * self.texture_atlas.sprite_scale.x):
            pygame.draw.line(self.window.surface, RED, (x, 0), (x, height))

        for y in range(0, height, self.texture_atlas.sprite_height * self.texture_atlas.sprite_scale.y):
            pygame.draw.line(self.window.surface, RED, (0, y), (width, y))

    def render_gui(self):
        if self.gui_mode == GuiMode.HIDE_ALL or self.gui_mode == GuiMode.HIDE_GUI:
            return

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

        # Render Layer Info
        self.window.surface.blit(self.layer_info, (BOX_OFFSET, self.window.get_height() * DRAW_PERCENTAGE * 0.9))

    def render_gui_textures(self):
        for button in self.buttons:
            button.render(self.window.surface)
        for button in self.scroll_buttons:
            button.render(self.window.surface)

    def render_collision(self):
        for x in range(self.n_textures_x):
            for y in range(self.n_textures_y):
                collision = self.level_data.get_collision(x + int(self.position.x), y + int(self.position.y))
                if collision.shape is CollisionShape.NONE:
                    continue

                render_position = Vector(self.position.x * self.texture_atlas.scaled_width,
                                         self.position.y * self.texture_atlas.scaled_height).as_int()

                if collision.shape is CollisionShape.CIRCLE:
                    destination = collision.center_position - render_position
                    pygame.draw.circle(self.window.surface, GREEN, destination.as_tuple(), collision.radius)

                elif collision.shape is CollisionShape.RECTANGLE:
                    destination = collision.center_position - render_position - Vector(
                        self.texture_atlas.scaled_width // 2, self.texture_atlas.scaled_height // 2)
                    pygame.draw.rect(self.window.surface, RED,
                                     (destination.x, destination.y, collision.radius * 2, collision.radius * 2))

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
        self.edit_level(position, self.current_layer, self.selected_texture)

    def remove_level(self, position: Vector):
        self.edit_level(position, self.current_layer, -1)

    def edit_level(self, position: Vector, layer: int, texture: int):
        # Get Level coordinates
        if position.y >= self.window.get_height() * DRAW_PERCENTAGE and self.gui_mode == GuiMode.HIDE_NONE:
            return
        x = position.x // self.texture_atlas.scaled_width + self.position.x
        y = position.y // self.texture_atlas.scaled_height + self.position.y
        self.level_data.place_texture(texture, int(x), int(y), layer)

    def change_collision(self, position: Vector):
        x = position.x // self.texture_atlas.scaled_width + self.position.x
        y = position.y // self.texture_atlas.scaled_height + self.position.y
        center_position = Vector(x * self.texture_atlas.scaled_width + self.texture_atlas.scaled_width * 0.5,
                                 y * self.texture_atlas.scaled_height + self.texture_atlas.scaled_height * 0.5)
        self.level_data.change_collision(int(x), int(y), center_position,
                                         (self.texture_atlas.scaled_width + self.texture_atlas.scaled_height) / 4)

    def change_collision_radius(self, position: Vector, motion):
        x = position.x // self.texture_atlas.scaled_width + self.position.x
        y = position.y // self.texture_atlas.scaled_height + self.position.y
        self.level_data.change_collision_radius(int(x), int(y), motion)

    def update_game_info(self):
        self.game_info.x, self.game_info.y = pygame.mouse.get_pos()
        m1, m2, m3 = pygame.mouse.get_pressed()
        self.game_info.fire_trigger.update(m1)

    def load_level(self):
        default = [("Level File", "*.lvl")]
        file = askopenfilename(filetypes=default, defaultextension="*.lvl")
        if file is None:
            return
        self.level_data = load_level(file)
        self.save_path = file

    def save_level(self):
        if self.save_path is None:
            default = [("Level File", "*.lvl")]
            file = asksaveasfile(filetypes=default, defaultextension="*.lvl")
            if file is None:
                return
            self.save_path = file.name

        self.level_data.save_level(self.save_path)
        print_debug(f"Saved level as {self.save_path}")
