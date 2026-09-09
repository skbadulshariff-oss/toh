import pygame

# Display Settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors (RGB)
BG_COLOR = (30, 30, 40)
PEG_COLOR = (180, 180, 180)
BASE_COLOR = (100, 100, 100)
TEXT_COLOR = (240, 240, 240)

DISK_COLORS = [
    (239, 71, 111),   # Pinkish Red
    (255, 209, 102),  # Yellow
    (6, 214, 160),    # Teal
    (17, 138, 178),   # Blue
    (7, 59, 76)       # Dark Navy
]

# Peg & Disk Configuration
NUM_DISKS = 3
PEG_WIDTH = 12
PEG_HEIGHT = 250
BASE_Y = 480
PEG_POSITIONS = [200, 400, 600]
MIN_DISK_WIDTH = 50
MAX_DISK_WIDTH = 170
DISK_HEIGHT = 24
