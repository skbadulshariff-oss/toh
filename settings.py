import pygame

# Display Settings
WIDTH, HEIGHT = 900, 650
FPS = 60

# --- Modern Synthwave Night Palette (RGB) ---
# Background Gradients
BG_TOP = (10, 12, 28)       # Deep Space Indigo
BG_BOTTOM = (25, 10, 45)    # Dark Royal Purple

# UI & Environment Elements
PANEL_BG = (35, 30, 60)      # Muted Violet Panel
PANEL_BORDER = (80, 50, 120)  # Lighter Purple Border
TEXT_COLOR = (230, 240, 255) # Soft Ice Blue
PEG_COLOR = (210, 215, 235)  # Misty Silver
PEG_GLOW = (130, 210, 255)   # Cyan Accent

# Interactive Element Colors
BTN_DEFAULT = (50, 40, 80)
BTN_HOVER = (80, 60, 120)
BTN_ACTIVE = (120, 80, 180)

# Vibrant modern disk colors (matching the theme)
# Add more colors to support up to 8 disks
DISK_COLORS = [
    (255, 61, 127),   # Radiant Pink
    (255, 180, 50),   # Bright Gold
    (50, 255, 180),   # Electric Teal
    (61, 127, 255),   # Intense Sky Blue
    (140, 80, 255),   # Deep Violet
    (255, 110, 60),   # Vivid Orange
    (100, 255, 100),  # Bright Green
    (255, 220, 100)   # Pale Yellow
]

# Peg & Disk Configuration
DEFAULT_DISKS = 3
MIN_DISKS = 3
MAX_DISKS = 8

PEG_WIDTH = 12
PEG_HEIGHT = 280
BASE_Y = 520
PEG_POSITIONS = [240, 450, 660]
MIN_DISK_WIDTH = 55
MAX_DISK_WIDTH = 190
DISK_HEIGHT = 26

# --- AI Speed Configuration ---
# 0.03 is very slow and smooth
AI_STEP_SPEED = 0.025
