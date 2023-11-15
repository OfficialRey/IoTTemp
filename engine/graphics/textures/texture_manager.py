from engine.graphics.textures.atlas import LevelAtlas, AnimationAtlas
from engine.graphics.textures.texture_animation import AnimationType

# Define Animations in Sprite Sheet

PLAYER = [AnimationType.IDLE, AnimationType.WALKING_E, None, AnimationType.ATTACK, AnimationType.DAMAGED,
          AnimationType.DEATH]
CURSOR = [AnimationType.GENERIC]

CENTIPEDE = [AnimationType.WALKING_E, AnimationType.WALKING_NE, AnimationType.WALKING_N, AnimationType.WALKING_NW,
             AnimationType.WALKING_W, AnimationType.WALKING_SW, AnimationType.WALKING_S, AnimationType.WALKING_SE]
CENTIPEDE_BODY = [None, None, None, None, None, None, None, None,
                  AnimationType.WALKING_E, AnimationType.WALKING_NE, AnimationType.WALKING_N, AnimationType.WALKING_NW,
                  AnimationType.WALKING_W, AnimationType.WALKING_SW, AnimationType.WALKING_S, AnimationType.WALKING_SE]


class TextureManager:
    # Class for loading and initializing all required textures of the game

    def __init__(self):
        self.level_textures = LevelAtlas("level", "level_textures.png", 16, 16)
        self.centipede = AnimationAtlas("enemies", "centipede.png", CENTIPEDE, 16, 16, time=0.2, loop=True)
        self.centipede_body = AnimationAtlas("enemies", "centipede.png", CENTIPEDE_BODY, 16, 16, time=0.2, loop=True)

        # Player
        self.cursor = AnimationAtlas("player", "target.png", CURSOR, 24, 24, time=0.2, loop=True)
        self.player = AnimationAtlas("player", "player.png", PLAYER, 16, 16, time=0.2, loop=True)
