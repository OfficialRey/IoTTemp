import os
from enum import Enum
from typing import Dict

import pygame.mixer

from engine.util.resources import get_resource_path


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


class SoundEngine:

    def __init__(self, sound_volume: float = 0.1, music_volume: float = 0.1):
        pygame.mixer.init()
        self.sound_path = os.path.join(get_resource_path(), "sound")
        self.music_path = os.path.join(get_resource_path(), "music")
        self.sounds: Dict[GameSound, pygame.mixer.Sound] = {}
        self.sound_volume = sound_volume
        self.music_volume = music_volume

        self._load_sounds()

    def _load_sounds(self):
        self.sounds = {}
        for game_sound in GameSound:
            path = os.path.join(self.sound_path, game_sound.get_file_name())
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.sound_volume)
            self.sounds[game_sound] = sound

    def get_sound(self, sound: GameSound):
        return self.sounds[sound]

    def play_sound(self, sound: GameSound):
        self.sounds[sound].play()

    def set_sound_volume(self, value):
        value = max(0, min(value, 1))
        for key in self.sounds.keys():
            self.sounds[key].set_volume(value)

    def play_music(self, music: GameMusic):
        path = os.path.join(self.music_path, music.get_file_name())
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops=-1)
