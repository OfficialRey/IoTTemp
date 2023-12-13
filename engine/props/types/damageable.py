from engine.core.vector import Vector
from engine.graphics.animation.animation import AnimationType
from engine.graphics.atlas.animation import AnimationAtlas
from engine.props.types.sprite import Sprite
from engine.sound.game_sound import GameSound, SoundMixer
from engine.world.collision import CollisionInformation

FLASH_TIME = 0.2

I_MELEE = 0.5
I_RANGED = 0.3


class Damageable(Sprite):

    def __init__(self, sound_mixer: SoundMixer, atlas: AnimationAtlas, world, max_health: int, attack: int, defense: int,
                 max_speed: float = 0, acceleration: float = 0, center_position: Vector = Vector(),
                 velocity: Vector = Vector()):
        super().__init__(atlas, max_speed, acceleration, center_position, velocity)
        self.sound_mixer = sound_mixer
        self.world = world
        self.max_health = max_health
        self.health = self.max_health
        self.attack = attack
        self.defense = defense
        self.triggered_death = False
        self.invincibility_time = 0

    def update(self, world, delta_time: float) -> None:
        self.invincibility_time -= delta_time
        super().update(world, delta_time)

    def apply_knock_back(self, direction: Vector, strength: float):
        self.accelerate_normalized(direction.normalize(), strength)

    def damage(self, value: float, collision_info: CollisionInformation, knock_back_strength: float = 5,
               melee_damage: bool = False):
        if self.invincibility_time > 0:
            return
        self.damage_true(value * self.get_damage_multiplier(), melee_damage)
        if collision_info is not None and melee_damage:
            self.apply_knock_back(collision_info.direction, knock_back_strength)

    def damage_true(self, value: float, melee_damage: bool = False):
        if self.invincibility_time > 0:
            return
        self.invincibility_time = I_MELEE if melee_damage else I_RANGED
        self.health -= value
        self.flash_image(self.invincibility_time)
        self.on_hit()

        if self.health <= 0:
            if not self.triggered_death:
                self.on_death()

    def play_death_animation(self):
        self.animation_manager.flash_time = 0
        self.triggered_death = True
        self.animation_manager.single_play = False
        self.animation_manager.update_animation_type(AnimationType.DEATH)
        self.animation_manager.update_current_animation(loop=False)
        self.animation_manager.current_animation.set_cycle_time(1)
        self.acceleration = 0
        self.velocity = Vector(0, 0)

    def collide_generic(self, other) -> CollisionInformation:
        if self.is_dead():
            return CollisionInformation()
        return super().collide_generic(other)

    def get_damage_multiplier(self):
        return 100 / (100 + self.defense)

    def is_dead(self) -> bool:
        return self.health <= 0

    def can_remove(self) -> bool:
        if not self.is_dead():
            return False
        if self.atlas.get_animation_data(AnimationType.DEATH) is not None:
            return self.animation_manager.is_animation_finished()
        return True

    def play_sound(self, sound: GameSound, direction: Vector = None):
        self.sound_mixer.play_sound(sound, direction)

    def on_death(self):
        self.play_death_animation()

    def on_hit(self):
        self.play_sound(GameSound.HURT, self.center_position - self.world.player.center_position)
