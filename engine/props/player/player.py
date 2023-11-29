import pygame

from engine.core.input_manager import InputManager
from engine.core.vector import Vector
from engine.graphics.textures.texture_animation import AnimationType
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.bullet.bullet import BulletType
from engine.props.player.cursor import Cursor
from engine.props.types.shooting_unit import ShootingUnit
from engine.world.camera import Camera


class Player(ShootingUnit):

    def __init__(self, texture_manager: TextureManager):
        super().__init__(texture_manager.player, texture_manager.bullets, 100, 20, 20, max_speed=200, acceleration=0.1,
                         shot_delay=0.5)
        self.input_manager = None
        self.cursor = Cursor(texture_manager)
        self.cursor.play_animation(AnimationType.GENERIC)

    def act(self, delta_time: float) -> None:
        super().act(delta_time)
        self.cursor.update(delta_time)

    # Format: [w, a, s, d, space, mouse_x, mouse_y, left_click, right_click]

    def handle_input(self, input_manager: InputManager, camera):
        position = Vector(input_manager.mouse_x, input_manager.mouse_y)
        self.cursor.set_position(position)
        self.accelerate((self.cursor.position - camera.get_relative_position(self)))

        if input_manager.left_click:
            self.shoot_bullet(BulletType.GENERIC, (self.cursor.position + camera.position) - self.position)

    def render(self, surface: pygame.Surface, camera: Camera) -> None:
        self.cursor.render(surface, camera)
        super().render(surface, camera)
