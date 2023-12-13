import pygame

from engine.core.vector import Vector
from engine.game_info.game_info import GameInformation
from engine.graphics.animation.animation import AnimationType
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.data import UnitData
from engine.props.player.cursor import Cursor
from engine.props.types.sprite import Sprite
from engine.props.types.unit import ShootingUnit
from engine.props.weapon.weapon import WeaponManager, Weapon
from engine.sound.game_sound import SoundMixer
from engine.world.camera import Camera
from engine.world.collision import CollisionInformation


class Player(ShootingUnit):

    def __init__(self, world, sound_mixer: SoundMixer, texture_manager: TextureManager, weapon_manager: WeaponManager,
                 data: UnitData, center_position: Vector):
        super().__init__(sound_mixer, texture_manager.player, world, [], weapon_manager.comet_gun.bullet_type,
                         data.get_health(), data.get_attack(), data.get_defense(), data.get_max_speed(),
                         data.get_acceleration(), 0, center_position=center_position, is_enemy=False)
        self.input_manager = None
        self.cursor = Cursor(texture_manager)
        self.cursor.play_animation(AnimationType.GENERIC)
        self.set_weapon(weapon_manager.comet_gun)

    def update(self, world, delta_time: float) -> None:
        self.cursor.update(world, delta_time)
        super().update(world, delta_time)

    def set_weapon(self, weapon: Weapon):
        self.bullet_type = weapon.bullet_type
        self.shot_delay = weapon.shot_delay

    def run_behaviour(self, world, delta_time: float):
        self.animate_rotation(self._get_cursor_world_position(world.camera))

    # Format: [w, a, s, d, space, mouse_x, mouse_y, left_click, right_click]

    def handle_input(self, game_info: GameInformation, camera, delta_time: float):
        position = Vector(game_info.x, game_info.y)
        self.cursor.set_position(position)
        self.accelerate_normalized(self.cursor.center_position - camera.get_relative_position(self), delta_time)

        if game_info.fire_trigger.held:
            vector = self._get_cursor_world_position(camera) - self.center_position

            animation_type = AnimationType.RANGED_ATTACK_W if vector.x < 0 else AnimationType.RANGED_ATTACK_E

            if self.shoot_bullet((self.cursor.get_render_position() - self.get_render_position(camera))):
                self.animation_manager.single_play_animation(animation_type)

    def render(self, surface: pygame.Surface, camera: Camera) -> None:
        self.cursor.render(surface, camera)
        super().render(surface, camera)

    def _get_cursor_world_position(self, camera: Camera):
        return self.cursor.center_position + camera.center_position - (camera.resolution / 2)

    def on_hit(self):
        pass

    def on_attack(self):
        pass

    def on_collision(self, other: Sprite, collision_info: CollisionInformation):
        pass
