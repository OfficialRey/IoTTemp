from engine.graphics.textures.atlas import LevelAtlas, AnimationAtlas
from engine.graphics.textures.texture_animation import AnimationType

# Define Animations of Sprite Sheet

SINGLE_SPRITE = [AnimationType.GENERIC]

BULLETS = [AnimationType.GENERIC for _ in range(25)]

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

    # TODO: Somewhere here colors are overridden

    def __init__(self):
        self.level_textures = LevelAtlas("level", "level_textures.png", 16, 16)
        self.centipede_head = AnimationAtlas("enemies", "centipede.png", CENTIPEDE, 16, 16, animation_time=0.1, loop=True,
                                             has_flash_image=True)
        self.centipede_body = AnimationAtlas("enemies", "centipede.png", CENTIPEDE_BODY, 16, 16, animation_time=0.1, loop=True,
                                             has_flash_image=True)

        # Player
        self.cursor = AnimationAtlas("player", "target.png", CURSOR, 24, 24, animation_time=0.2, loop=True)
        self.player = AnimationAtlas("player", "player.png", PLAYER, 16, 16, animation_time=0.2, loop=True, has_flash_image=True)

        # Calibration
        self.calibrator = AnimationAtlas("calibration", "calibration.png", SINGLE_SPRITE, 16, 16)

        # Widgets and Icons
        self.arrow_up = AnimationAtlas("widgets", "arrow_up.png", SINGLE_SPRITE, 16, 16)
        self.arrow_down = AnimationAtlas("widgets", "arrow_down.png", SINGLE_SPRITE, 16, 16)

        # Bullets
        self.bullets = AnimationAtlas("bullets", "bullets.png", BULLETS, 16, 16, animation_time=0.05, rotation_precision=2)

        self.game_textures = [
            # Level
            self.level_textures,

            # Enemy
            self.centipede_head,
            self.centipede_body,

            # Player
            self.player, self.cursor,

            # Calibration
            self.calibrator,

            # Bullets
            self.bullets
        ]

    def scale_textures(self, scale):
        for texture_atlas in self.game_textures:
            texture_atlas.set_scale(scale)

    def count_textures(self):
        count = 0
        for atlas in self.game_textures:
            if isinstance(atlas, AnimationAtlas):
                for animation in atlas.texture_animations:
                    count += len(animation.textures)
        return count
