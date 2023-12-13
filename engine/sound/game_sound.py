import os
from enum import Enum

import pygame.mixer

from engine.core.vector import Vector
from engine.util.resources import get_resource_path

MAX_SOUND_DISTANCE = 1200


class GameSound(Enum):
    # GUI

    GUI_HOVER = "gui_hover.wav",
    GUI_CONFIRM = "gui_confirm.wav",

    # DAMAGE
    HURT = "hurt.wav",
    DEATH = "death.wav",

    # SHOOTING
    LASER = "laser.wav",

    # EFFECTS
    POWER_UP = "power_up.wav",

    def get_file_name(self):
        return self.value[0]


class GameMusic(Enum):
    DEFAULT = "game_music_loop.wav",

    def get_file_name(self):
        return self.value[0]


class SoundMixer:
    def __init__(self, channels: int = 2, buffer: int = 1024, sound_volume: float = 0.1, music_volume: float = 0.1):
        pygame.mixer.init(channels=channels, buffer=buffer)

        # Path
        self.sound_path = os.path.join(get_resource_path(), "sound")
        self.music_path = os.path.join(get_resource_path(), "music")

        # Volume
        self.sound_volume = sound_volume
        self.music_volume = music_volume

        # Sound Mixing
        self.sounds = {}
        self._load_sounds()

    def get_sound(self, game_sound: GameSound):
        return self.sounds[game_sound]

    def play_sound(self, game_sound: GameSound, direction: Vector = None):
        if direction is None:
            self.play_non_directional_sound(game_sound)
            return

        self.play_directional_sound(game_sound, direction)

    def play_non_directional_sound(self, game_sound: GameSound):
        sound = self.sounds[game_sound]
        channel = pygame.mixer.find_channel(True)

        channel.set_volume(self.sound_volume)
        channel.play(sound)

    def play_directional_sound(self, game_sound: GameSound, direction: Vector):
        channel = pygame.mixer.find_channel(True)
        sound = self.sounds[game_sound]

        distance = direction.magnitude()
        if distance > 0:
            volume = max(0.0, self.sound_volume * (1 - (distance / MAX_SOUND_DISTANCE)))
            if direction.x > 0:
                left_volume = volume / 2
                right_volume = volume
            else:
                left_volume = volume
                right_volume = volume / 2
            channel.set_volume(left_volume, right_volume)
        else:
            channel.set_volume(self.sound_volume)

        channel.play(sound)

    def play_music(self, music: GameMusic):
        path = os.path.join(self.music_path, music.get_file_name())
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loops=-1)

    def _load_sounds(self):
        for game_sound in GameSound:
            path = os.path.join(self.sound_path, game_sound.get_file_name())
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.sound_volume)
            self.sounds[game_sound] = sound
