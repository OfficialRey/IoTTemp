import os
from enum import Enum
from typing import Dict

import pygame.mixer

from engine.util.resources import get_resource_path


class GameSound(Enum):
    # Format: File Name
    GUI_HOVER = "gui_hover.wav",
    GUI_CONFIRM = "gui_confirm.wav",

    def get_file_name(self):
        return self.value[0]


class GameMusic(Enum):
    pass


class Sound:

    def __init__(self, file_name: str, volume: float):
        self.path = os.path.join(get_resource_path(), os.path.join("sound", file_name))
        self.sound = pygame.mixer.Sound(self.path)
        self.set_volume(volume)

    def play_sound(self):
        self.sound.play()

    def stop_sound(self):
        self.sound.stop()

    def set_volume(self, value: float):
        self.sound.set_volume(value)


class SoundEngine:

    def __init__(self, sound_volume: float = 0.1, music_volume: float = 0.1):
        pygame.mixer.init()
        self.sounds: Dict[GameSound, Sound] = {}
        self.sound_volume = sound_volume
        self.music_volume = music_volume

        self._load_sounds()
        self.set_sound_volume(self.sound_volume)

    def _load_sounds(self):
        self.sounds = {}
        for sound in GameSound:
            self.sounds[sound] = Sound(sound.get_file_name(), 1)

    def get_sound(self, sound: GameSound):
        return self.sounds[sound]

    def play_sound(self, sound: GameSound):
        self.sounds[sound].play_sound()

    def set_sound_volume(self, value):
        value = max(0, min(value, 1))
        for key in self.sounds.keys():
            self.sounds[key].set_volume(value)
