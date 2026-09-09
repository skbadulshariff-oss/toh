import pygame
from settings import *

class Disk:
    def __init__(self, size, width, color):
        self.size = size
        self.width = width
        self.color = color
        self.rect = pygame.Rect(0, 0, width, DISK_HEIGHT)

class Game:
    def __init__(self):
        self.num_disks = DEFAULT_DISKS
        self.pegs = [[], [], []]
        self.selected_disk = None
        self.selected_peg_idx = None
        self.move_count = 0
        self.reset_game()

    def set_disk_count(self, count):
        """Set a new disk count (3-8) and reset."""
        self.num_disks = max(MIN_DISKS, min(MAX_DISKS, count))
        self.reset_game()

    def reset_game(self):
        self.pegs = [[], [], []]
        self.move_count = 0
        self.selected_disk = None
        
        # Create disks from largest to smallest on Peg 0
        # Dynamically calculate width scale based on num_disks
        width_step = (MAX_DISK_WIDTH - MIN_DISK_WIDTH) // max(1, self.num_disks - 1)
        
        for i in range(self.num_disks, 0, -1):
            width = MIN_DISK_WIDTH + (i - 1) * width_step
            color = DISK_COLORS[(i - 1) % len(DISK_COLORS)]
            disk = Disk(i, width, color)
            self.pegs[0].append(disk)
        self._update_disk_positions()

    def _update_disk_positions(self):
        for peg_idx, stack in enumerate(self.pegs):
            for level, disk in enumerate(stack):
                if disk != self.selected_disk:
                    x = PEG_POSITIONS[peg_idx] - disk.width // 2
                    y = BASE_Y - (level + 1) * DISK_HEIGHT
                    disk.rect.topleft = (x, y)

    def select_disk(self, pos):
        for i, stack in enumerate(self.pegs):
            if stack:
                top_disk = stack[-1]
                if top_disk.rect.collidepoint(pos):
                    self.selected_disk = top_disk
                    self.selected_peg_idx = i
                    return True # Return success for sound
        return False

    def release_disk(self, pos):
        """Attempts to release disk. Returns (bool: moved, bool: puzzle_solved)."""
        if not self.selected_disk:
            return False, False

        target_peg = min(range(len(PEG_POSITIONS)), key=lambda i: abs(PEG_POSITIONS[i] - pos[0]))
        
        moved = False
        solved = False

        # Validate move: Target peg must be empty OR top disk must be larger
        if not self.pegs[target_peg] or self.pegs[target_peg][-1].size > self.selected_disk.size:
            self.pegs[self.selected_peg_idx].pop()
            self.pegs[target_peg].append(self.selected_disk)
            if self.selected_peg_idx != target_peg:
                self.move_count += 1
                moved = True
        
        solved = self.is_won()
        
        self.selected_disk = None
        self._update_disk_positions()
        
        return moved, solved

    def move_disk(self, from_peg, to_peg):
        """Programmatic move for AI solver"""
        if self.pegs[from_peg]:
            disk = self.pegs[from_peg].pop()
            self.pegs[to_peg].append(disk)
            self.move_count += 1
            self._update_disk_positions()

    def is_won(self):
        return len(self.pegs[2]) == self.num_disks
