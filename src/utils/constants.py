"""
Constants - Game configuration constants
"""

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TITLE = "Joust"

# Game settings
FPS = 60
GRAVITY = 0.5
FLAP_POWER = 12
MAX_VERTICAL_SPEED = 15
HORIZONTAL_SPEED = 5
HORIZONTAL_ACCELERATION = 0.5
HORIZONTAL_DECELERATION = 0.3
MAX_HORIZONTAL_SPEED = 8

# Player settings
PLAYER_START_LIVES = 3
PLAYER_INVINCIBILITY_TIME = 2000  # milliseconds
PLAYER_RESPAWN_TIME = 1500  # milliseconds

# Enemy settings
ENEMY_SPAWN_DELAY = 3000  # milliseconds between waves
PTERODACTYL_SPAWN_TIME = 30000  # milliseconds before pterodactyl appears
ENEMY_TYPES = {
    "BOUNDER": {
        "speed": 3,
        "points": 250,
        "color": "red"
    },
    "HUNTER": {
        "speed": 4.5,
        "points": 500,
        "color": "gray"
    },
    "SHADOW_LORD": {
        "speed": 6,
        "points": 1500,
        "color": "blue"
    },
    "PTERODACTYL": {
        "speed": 7,
        "points": 1000,
        "color": "purple"
    }
}

# Egg settings
EGG_LIFETIME = 10000  # milliseconds before hatching
EGG_POINTS = 500
EGG_COLLECT_ALL_BONUS = 2000

# Wave settings
WAVE_SETTINGS = {
    # Wave number: (num_bounders, num_hunters, num_shadow_lords)
    1: (3, 0, 0),
    2: (4, 0, 0),
    3: (5, 0, 0),
    4: (3, 2, 0),
    5: (2, 3, 0),
    6: (3, 3, 0),
    7: (2, 3, 1),
    8: (3, 3, 1),
    9: (2, 4, 1),
    10: (3, 4, 2),
    # After wave 10, increase difficulty linearly
}

# Lava settings
LAVA_HEIGHT = 40
LAVA_Y_POSITION = SCREEN_HEIGHT - LAVA_HEIGHT

# Platform settings
PLATFORM_HEIGHT = 20
PLATFORM_POSITIONS = [
    # (x, y, width) - y is from the top
    (120, 170, 200),  # Top left platform
    (SCREEN_WIDTH - 320, 170, 200),  # Top right platform
    (240, 330, 800),  # Middle platform
    (120, 490, 200),  # Bottom left platform
    (SCREEN_WIDTH - 320, 490, 200),  # Bottom right platform
]

# Bottom platform settings - changes with level
# Format: level: [(x, width), (x, width), ...]
# For each level, defines sections of the bottom platform
BOTTOM_PLATFORM_Y = SCREEN_HEIGHT - LAVA_HEIGHT - PLATFORM_HEIGHT - 10  # Just above lava
BOTTOM_PLATFORM_CONFIGS = {
    # Level 1: Full platform across the bottom
    1: [(0, SCREEN_WIDTH)],
    
    # Level 2: Two large sections
    2: [(0, SCREEN_WIDTH * 0.45), (SCREEN_WIDTH * 0.55, SCREEN_WIDTH * 0.45)],
    
    # Level 3: Three medium sections
    3: [(0, SCREEN_WIDTH * 0.3), 
        (SCREEN_WIDTH * 0.35, SCREEN_WIDTH * 0.3), 
        (SCREEN_WIDTH * 0.7, SCREEN_WIDTH * 0.3)],
    
    # Level 4: Four smaller sections
    4: [(0, SCREEN_WIDTH * 0.2), 
        (SCREEN_WIDTH * 0.25, SCREEN_WIDTH * 0.2), 
        (SCREEN_WIDTH * 0.5, SCREEN_WIDTH * 0.2), 
        (SCREEN_WIDTH * 0.75, SCREEN_WIDTH * 0.25)],
    
    # Level 5+: Small scattered platforms
    5: [(0, SCREEN_WIDTH * 0.15), 
        (SCREEN_WIDTH * 0.25, SCREEN_WIDTH * 0.15), 
        (SCREEN_WIDTH * 0.5, SCREEN_WIDTH * 0.15), 
        (SCREEN_WIDTH * 0.75, SCREEN_WIDTH * 0.15)],
    
    # Level 6+: Minimal platforms
    6: [(SCREEN_WIDTH * 0.1, SCREEN_WIDTH * 0.1), 
        (SCREEN_WIDTH * 0.3, SCREEN_WIDTH * 0.1), 
        (SCREEN_WIDTH * 0.5, SCREEN_WIDTH * 0.1), 
        (SCREEN_WIDTH * 0.7, SCREEN_WIDTH * 0.1), 
        (SCREEN_WIDTH * 0.9, SCREEN_WIDTH * 0.1)],
}

# Score settings
SCORE_EXTRA_LIFE = 10000  # Score needed for an extra life

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
LAVA_COLOR = (255, 69, 0)
