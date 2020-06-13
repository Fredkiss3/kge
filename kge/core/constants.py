from kge.utils.color import Color
from kge.utils.condition import Condition

# Conditions
ALWAYS = Condition(True)
NEVER = Condition(False)

# RENDER INFOS
MAX_ZOOM = 10.0
MIN_ZOOM = 1 / 10
DEFAULT_RESOLUTION = 1280, 720
WINDOW_POSITION = 100, 35
DEFAULT_FPS = 60
REFERENCE_PIXEL_RATIO = 64
DEFAULT_PIXEL_RATIO = 64
IS_FULLSCREEN = False
IS_RESIZABLE = True
MAX_LAYERS = 20

# COLORS
RED = Color(255, 0, 0, 1)
YELLOW = Color(255, 255, 0, 1)
GREEN = Color(0, 255, 0, 1)
BLUE = Color(0, 0, 125, 1)
WHITE = Color(255, 255, 255, 1)
GREY = Color(127, 127, 127, 1)
LIGHTGREY = Color(180, 180, 180, 127 / 255)
DARKGREY = Color(127, 127, 127, 127 / 255)
BLACK = Color(0, 0, 0, 1)
MAGENTA = Color(255, 71, 182, 1)
PURPLE = Color(187, 0, 255, 1)

# PHYSICS
FIXED_FPS = 50
FIXED_DELTA_TIME = 1 / FIXED_FPS

# SPRITE SIZE
DEFAULT_SPRITE_SIZE = DEFAULT_PIXEL_RATIO
DEFAULT_SPRITE_RESOLUTION = DEFAULT_SPRITE_SIZE, DEFAULT_SPRITE_SIZE

if __name__ == '__main__':
    print(RED)
