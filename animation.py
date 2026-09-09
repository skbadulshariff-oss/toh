import pygame
from settings import *
import os

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font_main = pygame.font.SysFont("Avenir Next", 22, bold=True)
            self.font_big = pygame.font.SysFont("Avenir Next", 60, bold=True)
            self.font_btn = pygame.font.SysFont("Avenir Next", 28, bold=True)
        except:
            self.font_main = pygame.font.SysFont("Consolas", 20, bold=True)
            self.font_big = pygame.font.SysFont("Consolas", 50, bold=True)
            self.font_btn = pygame.font.SysFont("Consolas", 24, bold=True)
            
        self.bg_surface = self._create_gradient_background()
        
        # Define interaction buttons for selection screen
        self.buttons = []
        for i in range(MIN_DISKS, MAX_DISKS + 1):
            # x, y, w, h
            rect = pygame.Rect(180 + (i-3) * 95, 300, 75, 75)
            self.buttons.append({'rect': rect, 'count': i})

        # --- Sound Initialization ---
        pygame.mixer.init()
        self.sounds = {}
        sound_files = {
            'select': 'select.wav',
            'move': 'move.wav',
            'error': 'error.wav',
            'success': 'success.wav'
        }
        
        for name, file in sound_files.items():
            if os.path.exists(file):
                self.sounds[name] = pygame.mixer.Sound(file)
                # Lower volume slightly for comfort
                self.sounds[name].set_volume(0.4) 
            else:
                print(f"WARNING: Sound file {file} not found. Running without {name} sound.")
                self.sounds[name] = None # Placeholder

    def _create_gradient_background(self):
        """Pre-renders a smooth modern vertical gradient"""
        bg = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
            g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
            b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
            pygame.draw.line(bg, (r, g, b), (0, y), (WIDTH, y))
        return bg

    def play_sound(self, name):
        if self.sounds.get(name):
            self.sounds[name].play()

    def draw_selection_menu(self):
        """Draws the pre-game disk count selection screen."""
        self.screen.blit(self.bg_surface, (0, 0))
        
        # Title
        title_surf = self.font_big.render("TOWER OF HANOI", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 120))
        self.screen.blit(title_surf, title_rect)
        
        sub_surf = self.font_main.render("Select number of disks to begin", True, PEG_GLOW)
        sub_rect = sub_surf.get_rect(center=(WIDTH // 2, 190))
        self.screen.blit(sub_surf, sub_rect)

        # Draw Buttons
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            rect = btn['rect']
            color = BTN_DEFAULT
            
            # Hover detection
            if rect.collidepoint(mouse_pos):
                color = BTN_HOVER
            
            pygame.draw.rect(self.screen, color, rect, border_radius=12)
            pygame.draw.rect(self.screen, PANEL_BORDER, rect, width=2, border_radius=12)
            
            # Button Text
            text_surf = self.font_btn.render(str(btn['count']), True, TEXT_COLOR)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)

    def handle_menu_click(self, pos):
        """Checks if a button was clicked on the menu."""
        for btn in self.buttons:
            if btn['rect'].collidepoint(pos):
                self.play_sound('select')
                return btn['count']
        return None

    def draw_game(self, game, is_ai_running, animating_disk=None):
        # 1. Draw Background
        self.screen.blit(self.bg_surface, (0, 0))

        # 2. Draw Main Platform Base with styled border
        platform_rect = pygame.Rect(100, BASE_Y, 700, 24)
        pygame.draw.rect(self.screen, PANEL_BG, platform_rect, border_radius=8)
        pygame.draw.rect(self.screen, PANEL_BORDER, platform_rect, width=2, border_radius=8)

        # 3. Draw Pegs with a subtle subtle internal glow
        for pos in PEG_POSITIONS:
            peg_rect = pygame.Rect(pos - PEG_WIDTH // 2, BASE_Y - PEG_HEIGHT, PEG_WIDTH, PEG_HEIGHT)
            # Peg Shaft
            pygame.draw.rect(self.screen, PEG_COLOR, peg_rect, border_radius=4)
            # Small Accent / 'Light' top dot
            pygame.draw.circle(self.screen, PEG_GLOW, (pos, BASE_Y - PEG_HEIGHT + 6), 3)

        # 4. Draw Static Disks (Not being dragged/animated)
        for stack in game.pegs:
            for disk in stack:
                if disk != game.selected_disk and disk != animating_disk:
                    pygame.draw.rect(self.screen, disk.color, disk.rect, border_radius=6)

        # 5. Draw Currently Animating AI Disk
        if animating_disk:
            pygame.draw.rect(self.screen, animating_disk.color, animating_disk.rect, border_radius=6)

        # 6. Draw Mouse Dragged Disk (User manual control)
        if game.selected_disk:
            mouse_pos = pygame.mouse.get_pos()
            game.selected_disk.rect.center = mouse_pos
            pygame.draw.rect(self.screen, game.selected_disk.color, game.selected_disk.rect, border_radius=6)

        # 7. Draw Modern Top Header Panel (HUD)
        header_rect = pygame.Rect(0, 0, WIDTH, 55)
        pygame.draw.rect(self.screen, PANEL_BG, header_rect)
        pygame.draw.line(self.screen, PANEL_BORDER, (0, 55), (WIDTH, 55), width=2)
        
        # Info Text
        disks_str = f"DISKS: {game.num_disks}"
        moves_str = f"MOVES: {game.move_count}"
        ctrl_str = "'R': Reset | 'SPACE': AI | 'ESC': Menu"
        
        if is_ai_running:
            ctrl_str = "AI SOLVER ACTIVE..."
        elif game.is_won():
            ctrl_str = "SOLVED! Press ESC for Menu"
            
        final_info = f"{disks_str} | {moves_str} | {ctrl_str}"
        text_surface = self.font_main.render(final_info, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 27))
        self.screen.blit(text_surface, text_rect)
