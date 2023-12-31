from engine.core.vector import Vector
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.bullet.bullet import BulletType
from engine.props.data import UnitData
from engine.props.enemy.ai.ai import ShootingAI
from engine.props.enemy.enemy import ShootingEnemy
from engine.props.types.sprite import Sprite
from engine.sound.game_sound import SoundMixer, GameSound
from engine.world.collision import CollisionInformation

TARGET_DISTANCE = 350


class ShootingSpider(ShootingEnemy):
    def __init__(self, world, sound_mixer: SoundMixer, texture_manager: TextureManager, bullet_type: BulletType,
                 center_position: Vector):
        super().__init__(sound_mixer, texture_manager.spider, world,
                         [GameSound.SPIDER_AMBIENCE_0, GameSound.SPIDER_AMBIENCE_1, GameSound.SPIDER_AMBIENCE_2],
                         bullet_type, UnitData.SHOOTING_SPIDER, center_position)
        self.ai = ShootingAI(self)

    def run_behaviour(self, world, delta_time: float):
        self.ai.run(world, delta_time)
        self.animate_rotation(world.player.center_position)

    def on_attack(self):
        pass

    def on_collision(self, other: Sprite, collision_info: CollisionInformation):
        pass
