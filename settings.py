# settings.py

import os

# window
os.environ['SDL_VIDEO_WINDOW_POS'] = "1920,0"
DISPLAY_SIZE        = (1200, 675)
FOV                 = 60
NEAR_PLANE, FAR_PLANE = 0.1, 1000.0

# movement
MOVE_SPEED          = 0.5       # units per second
MOUSE_SENSITIVITY   = 0.2       # degrees per pixel

# grid & collision
GRID_EXTENT         = 20        # how far the grid extends in X/Z
GROUND_Y            = -1        # Y‑level of the grid
BASE_HALF           = 1.0
MIN_X, MAX_X        = -BASE_HALF, BASE_HALF
MIN_Z, MAX_Z        = -BASE_HALF, BASE_HALF
OBSTACLE_HEIGHT     = 2.0

# jumping
CAMERA_HEIGHT       = 0.05       # eye’s y‑offset above GROUND_Y
JUMP_SPEED          = 5.0
GRAVITY             = 15.0
JUMP_INTERVAL       = 0.5       # seconds between jumps
