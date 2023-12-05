from engine.core.vector import Vector
from engine.graphics.animation.animation import AnimationType
from engine.graphics.atlas.animation import AnimationAtlas
from engine.graphics.atlas.bullet import BulletAtlas
from engine.graphics.atlas.level import LevelAtlas
from engine.props.bullet.bullet import BulletType

# Define Animations of Sprite Sheet

SINGLE_SPRITE = [AnimationType.GENERIC]

BULLETS = [element for element in BulletType]

PLAYER = [AnimationType.IDLE, AnimationType.WALKING_E, None, AnimationType.RANGED_ATTACK, AnimationType.DAMAGED,
          AnimationType.DEATH]
CURSOR = [AnimationType.GENERIC]

CENTIPEDE = [AnimationType.WALKING_E, AnimationType.WALKING_NE, AnimationType.WALKING_N, AnimationType.WALKING_NW,
             AnimationType.WALKING_W, AnimationType.WALKING_SW, AnimationType.WALKING_S, AnimationType.WALKING_SE]

CENTIPEDE_BODY = [None, None, None, None, None, None, None, None,
                  AnimationType.WALKING_E, AnimationType.WALKING_NE, AnimationType.WALKING_N, AnimationType.WALKING_NW,
                  AnimationType.WALKING_W, AnimationType.WALKING_SW, AnimationType.WALKING_S, AnimationType.WALKING_SE]

SPIDER = [AnimationType.IDLE, AnimationType.WALKING_E, AnimationType.RANGED_ATTACK, AnimationType.MELEE_ATTACK,
          AnimationType.DEATH]


class TextureManager:
    # Class for loading and initializing all required textures of the game
    def __init__(self):
        # Level Textures
        self.level_textures = LevelAtlas("level", "level_textures.png", 16, 16)

        # Player
        self.cursor = AnimationAtlas("player", "target.png", CURSOR, 24, 24, animation_time=0.2)
        self.cursor.scale_textures(Vector(2, 2))
        self.player = AnimationAtlas("player", "player.png", PLAYER, 16, 16, animation_time=0.2)

        # Enemies
        self.centipede_head = AnimationAtlas("enemies", "centipede.png", CENTIPEDE, 16, 16, animation_time=0.1)
        self.centipede_body = AnimationAtlas("enemies", "centipede.png", CENTIPEDE_BODY, 16, 16, animation_time=0.1)
        self.spider = AnimationAtlas("enemies", "spider.png", SPIDER, 16, 16, animation_time=0.1)

        # Calibration
        self.calibrator = AnimationAtlas("calibration", "calibration.png", SINGLE_SPRITE, 16, 16)

        # Widgets and Icons
        self.arrow_up = AnimationAtlas("widgets", "arrow_up.png", SINGLE_SPRITE, 16, 16)
        self.arrow_down = AnimationAtlas("widgets", "arrow_down.png", SINGLE_SPRITE, 16, 16)

        # Bullets
        self.bullets = BulletAtlas("bullets", "bullets.png", 16, 16, BULLETS,
                                   animation_time=0.05, rotation_precision=10)

        self.game_textures = [
            # Level
            self.level_textures,

            # Player
            self.player,

            # Enemy
            self.centipede_head,
            self.centipede_body,
            self.spider,

            # Calibration
            self.calibrator,

            # Bullets
            self.bullets
        ]

    def scale_textures(self, scale):
        for texture_atlas in self.game_textures:
            texture_atlas.scale_textures(scale)

    def count_textures(self):
        count = 0
        for atlas in self.game_textures:
            count += atlas.count_surfaces()
        return count
