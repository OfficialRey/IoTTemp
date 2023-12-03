import pygame

from engine.core.input_manager import InputManager
from engine.core.vector import Vector
from engine.graphics.textures.texture_animation import AnimationType
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.bullet.bullet import BulletType
from engine.props.data import UnitData
from engine.props.player.cursor import Cursor
from engine.props.types.unit import ShootingUnit
from engine.sound.game_sound import SoundEngine
from engine.world.camera import Camera


class Player(ShootingUnit):

    def __init__(self, texture_manager: TextureManager, data: UnitData):
        super().__init__(texture_manager.player, texture_manager.bullets, data.get_health(), data.get_attack(),
                         data.get_defense(), data.get_shot_delay(), data.get_max_speed(), data.get_acceleration())
        self.input_manager = None
        self.cursor = Cursor(texture_manager)
        self.cursor.play_animation(AnimationType.GENERIC)

    def act(self, world, delta_time: float) -> None:
        super().run_behaviour(world, delta_time)
        self.cursor.update(world, delta_time)

    # Format: [w, a, s, d, space, mouse_x, mouse_y, left_click, right_click]

    def handle_input(self, input_manager: InputManager, camera, delta_time: float):
        position = Vector(input_manager.mouse_x, input_manager.mouse_y)
        self.cursor.set_position(position)
        self.accelerate((self.cursor.get_center_position() - camera.get_relative_position(self)), delta_time)

        if input_manager.left_click:
            self.shoot_bullet(BulletType.PLASMA, (self.cursor.get_center_position() + camera.position) - self.position)

    def render(self, surface: pygame.Surface, camera: Camera) -> None:
        self.cursor.render(surface, camera)
        super().render(surface, camera)
