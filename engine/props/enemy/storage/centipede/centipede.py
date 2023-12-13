from engine.core.vector import Vector
from engine.graphics.animation.animation_manager import AnimationManager
from engine.graphics.textures.texture_manager import TextureManager
from engine.props.data import UnitData
from engine.props.enemy.ai.centipede_ai import CentipedeAI, CentipedeState
from engine.props.enemy.enemy import MeleeEnemy
from engine.props.types.sprite import Sprite
from engine.props.types.unit import Unit
from engine.sound.game_sound import SoundMixer
from engine.world.collision import CollisionInformation


class Centipede(MeleeEnemy):
    centipede_state: CentipedeState

    def __init__(self, world, sound_mixer: SoundMixer, texture_manager: TextureManager, center_position: Vector,
                 previous_segment: Unit = None):
        super().__init__(sound_mixer, texture_manager.centipede_head, world, UnitData.CENTIPEDE, center_position)
        self.centipede_head = texture_manager.centipede_head
        self.centipede_body = texture_manager.centipede_body

        self.previous_segment = previous_segment
        self.ai = CentipedeAI(self)
        self.set_state(CentipedeState.HEAD if self.previous_segment is None else CentipedeState.BODY)

    def set_state(self, state: CentipedeState):
        self.centipede_state = state

        if self.centipede_state is CentipedeState.HEAD:
            self.animation_manager = AnimationManager(self.centipede_head)

        elif self.centipede_state is CentipedeState.BODY:
            self.animation_manager = AnimationManager(self.centipede_body)

    def run_behaviour(self, world, delta_time: float):
        self.ai.run(world, delta_time)

    def on_collision(self, other: Sprite, collision_info: CollisionInformation):
        pass
