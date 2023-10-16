from enum import Enum

import pygame.draw

from engine.core.window import Window
from engine.graphics.textures.texture import LevelAtlas
from engine.util.constants import RED, WHITE
from engine.world.level_data import LevelData

from tkinter import Tk
from tkinter.filedialog import askopenfilename

DRAW_PERCENTAGE = 0.7
GRAPHICS_PER_ROW = 10
GRAPHICS_LOADED = GRAPHICS_PER_ROW * 2
EDGE_DISTANCE = 20


class EditorStates(Enum):
    FILE_SELECT = 0,
    EDITING = 1


class LevelEditor:
    texture_atlas: LevelAtlas
    level_data: LevelData

    def __init__(self):
        self.window = Window(width=1080, height=720, full_screen=False)
        self.window.change_dimensions(full_screen=False)

        # Editor Parameters
        self.done = False
        self.zoom = 5
        self.texture_atlas = None
        self.level_data = None

        self.selected_texture = 0
        self.draw_row = 0
        self.draw_textures = []

    def run(self):
        self.select_textures()
        self.create_world()

        while not self.done:
            self.check_events()
            self.render()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_input(event)

    def render(self):
        self.render_world()
        self.render_grid()
        self.render_draw_textures()
        pygame.display.flip()

    def render_world(self):
        for x in range(0, self.level_data.width):
            for y in range(0, self.level_data.height):
                texture_id = self.level_data.get_texture_id(x, y)
                if texture_id >= 0:
                    texture = self.texture_atlas[texture_id]
                    destination = (
                        x * self.texture_atlas.sprite_width * self.zoom,
                        y * self.texture_atlas.sprite_height * self.zoom)
                    self.window.surface.blit(texture.image, destination)

    def render_grid(self):
        for x in range(0, self.window.width, self.texture_atlas.sprite_width * self.zoom):
            pygame.draw.line(self.window.surface, RED, (x, 0), (x, self.window.height * DRAW_PERCENTAGE))

        for y in range(0, int(self.window.height * DRAW_PERCENTAGE), self.texture_atlas.sprite_height * self.zoom):
            pygame.draw.line(self.window.surface, RED, (0, y), (self.window.width, y))

    def render_draw_textures(self):
        self.window.surface.fill(WHITE,
                                       (0, self.window.height * DRAW_PERCENTAGE, self.window.width, self.window.height))
        x_distance = self.window.width - EDGE_DISTANCE * 2
        texture_distance = x_distance // (len(self.draw_textures) / 2)
        for i in range(len(self.draw_textures)):
            x_pos = EDGE_DISTANCE + i * texture_distance
            y_pos = self.window.height * DRAW_PERCENTAGE + EDGE_DISTANCE
            if i >= GRAPHICS_PER_ROW:
                y_pos = y_pos + self.draw_textures[i].get_height() * 1.2
                x_pos = EDGE_DISTANCE + (i - 10) * texture_distance
            self.window.surface.blit(self.draw_textures[i], (x_pos, y_pos))

    def create_world(self):
        print("World Creation:")
        # world_name = input("World Name:")
        # width = int(input("Width:"))
        # height = int(input("Height:"))
        world_name = "Test"
        width = 200
        height = 200
        self.level_data = LevelData(self.texture_atlas, world_name, width, height)

    def select_textures(self):
        while self.texture_atlas is None:
            Tk().withdraw()
            filename = askopenfilename()
            sprite_width = int(input("Sprite Width:"))
            sprite_height = int(input("Sprite Height:"))
            self.texture_atlas = LevelAtlas(filename, sprite_width, sprite_height)
        self.update_draw_textures()

    def update_draw_textures(self):
        if self.draw_row < 0:
            self.draw_row = 0
        while self.draw_row * GRAPHICS_LOADED >= len(self.texture_atlas.base_textures):
            self.draw_row -= 1

        self.draw_textures = []
        for i in range(self.draw_row * GRAPHICS_LOADED,
                       min(self.draw_row * GRAPHICS_LOADED + GRAPHICS_LOADED, len(self.texture_atlas.base_textures))):
            self.draw_textures.append(self.texture_atlas.base_textures[i].base_image)

        for i in range(len(self.draw_textures)):
            self.draw_textures[i] = pygame.transform.scale(
                self.draw_textures[i],
                (self.draw_textures[i].get_width() * 4,
                 self.draw_textures[i].get_height() * 4)
            )

    def select_texture(self):
        pass

    def place_texture(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y < self.window.height * DRAW_PERCENTAGE:
            target_x = mouse_x // (self.texture_atlas.sprite_width * self.zoom)
            target_y = mouse_y // (self.texture_atlas.sprite_height * self.zoom)
            self.level_data.place_texture(self.selected_texture, target_x, target_y)

    def handle_mouse_input(self, event):
        mouse_y = pygame.mouse.get_pos()[1]
        if mouse_y < self.window.height * DRAW_PERCENTAGE:

            # Editor Controls
            if event.button == 1:
                self.place_texture()

        else:

            # Texture Controls
            if event.button == 1:
                self.select_texture()
            elif event.button == 4:
                self.draw_row -= 1
                self.update_draw_textures()
            elif event.button == 5:
                self.draw_row += 1
                self.update_draw_textures()


if __name__ == '__main__':
    # Launch Level Editor
    editor = LevelEditor()
    editor.run()
