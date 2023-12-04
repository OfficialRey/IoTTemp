from engine.graphics.animation.animation import AnimationData, AnimationAtlas
from engine.graphics.textures.texture import Texture


class AnimationManager:

    def __init__(self, animation_data: AnimationData):
        self.animation_data = animation_data

        self.timer = 0
        self.count = 0

    def update(self, delta_time: float):
        self.timer += delta_time
        if self.timer >= self.animation_data.animation_time:
            self.count += 1
            self.timer -= self.animation_data.animation_time
            if self.count >= self.animation_data.length:
                if self.animation_data.loop:
                    self.count = 0
                else:
                    self.count -= 1

    def offset_animation(self, value: float):
        self.count = int(value / self.animation_data.animation_time)
        self.timer = value % self.animation_data.animation_time

    def get_texture(self, animation_atlas: AnimationAtlas) -> Texture:
        return animation_atlas.textures[self.animation_data.start_index + self.count]
