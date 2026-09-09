import pygame
import sys
from settings import *
from game import Game
from ai import TowerOfHanoiAI
from animation import Renderer

# Application States
STATE_MENU = 0
STATE_GAME = 1

def get_peg_top_y(game, peg_idx):
    """Calculate the landing Y coordinate for a peg stack"""
    stack_height = len(game.pegs[peg_idx])
    return BASE_Y - (stack_height + 1) * DISK_HEIGHT

def main():
    pygame.init()
    # Updated resolution from settings.py
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tower of Hanoi - Modern AI Solver")
    clock = pygame.time.Clock()

    game = Game()
    ai = TowerOfHanoiAI()
    renderer = Renderer(screen)

    # App state management
    app_state = STATE_MENU
    
    ai_moves = []
    is_ai_running = False
    puzzle_solved_played = False # Track success sound

    # Animation State Variables
    animating_disk = None
    anim_step = 0  # 0: Up, 1: Across, 2: Down
    anim_progress = 0.0
    ANIM_SPEED = AI_STEP_SPEED
    
    start_pos = (0, 0)
    target_pos = (0, 0)
    current_move = None

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- Menu Event Handling ---
            if app_state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    selected_count = renderer.handle_menu_click(event.pos)
                    if selected_count:
                        # Set disks, reset game, switch to game state
                        game.set_disk_count(selected_count)
                        app_state = STATE_GAME
                        puzzle_solved_played = False
                        is_ai_running = False

            # --- Game Event Handling ---
            elif app_state == STATE_GAME:
                if event.type == pygame.MOUSEBUTTONDOWN and not is_ai_running and not animating_disk:
                    if event.button == 1:
                        # Ignore mouse interaction if near the header panel
                        if event.pos[1] > 60:
                            selected = game.select_disk(event.pos)
                            if selected:
                                renderer.play_sound('select')

                elif event.type == pygame.MOUSEBUTTONUP and not is_ai_running and not animating_disk:
                    if event.button == 1:
                        if game.selected_disk:
                            moved, solved = game.release_disk(event.pos)
                            
                            if moved:
                                renderer.play_sound('move')
                                if solved and not puzzle_solved_played:
                                    renderer.play_sound('success')
                                    puzzle_solved_played = True
                            else:
                                # Invalid move or same peg release
                                renderer.play_sound('error')

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Sound for reset
                        renderer.play_sound('select')
                        game.reset_game()
                        is_ai_running = False
                        ai_moves = []
                        animating_disk = None
                        puzzle_solved_played = False

                    elif event.key == pygame.K_ESCAPE:
                        # Return to Menu
                        renderer.play_sound('select')
                        app_state = STATE_MENU
                        is_ai_running = False
                        ai_moves = []
                        animating_disk = None

                    elif event.key == pygame.K_SPACE and not is_ai_running and not animating_disk:
                        renderer.play_sound('select')
                        game.reset_game()
                        ai_moves = ai.get_solution(game.num_disks)
                        is_ai_running = True
                        puzzle_solved_played = False

        # Draw current state
        if app_state == STATE_MENU:
            renderer.draw_selection_menu()
        
        elif app_state == STATE_GAME:
            # AI Move Queue & Interpolation Controller
            if is_ai_running and not animating_disk and ai_moves:
                current_move = ai_moves.pop(0)
                from_peg, to_peg = current_move
                
                animating_disk = game.pegs[from_peg].pop()
                anim_step = 0
                anim_progress = 0.0
                
                # Start position
                start_pos = (PEG_POSITIONS[from_peg] - animating_disk.width // 2, animating_disk.rect.y)
                # Peak clearance height
                clear_y = BASE_Y - PEG_HEIGHT - DISK_HEIGHT * 2
                target_pos = (start_pos[0], clear_y)

            # Smooth Arc Trajectory Physics
            if animating_disk:
                anim_progress += ANIM_SPEED
                
                # Interpolate Current Position
                progress = min(1.0, anim_progress)
                cur_x = start_pos[0] + (target_pos[0] - start_pos[0]) * progress
                cur_y = start_pos[1] + (target_pos[1] - start_pos[1]) * progress
                animating_disk.rect.topleft = (int(cur_x), int(cur_y))

                if anim_progress >= 1.0:
                    anim_progress = 0.0
                    from_peg, to_peg = current_move

                    if anim_step == 0:
                        # Move Across to Target Peg
                        anim_step = 1
                        start_pos = (animating_disk.rect.x, animating_disk.rect.y)
                        target_pos = (PEG_POSITIONS[to_peg] - animating_disk.width // 2, animating_disk.rect.y)

                    elif anim_step == 1:
                        # Drop Down onto Target Peg
                        anim_step = 2
                        start_pos = (animating_disk.rect.x, animating_disk.rect.y)
                        landing_y = get_peg_top_y(game, to_peg)
                        target_pos = (animating_disk.rect.x, landing_y)

                    elif anim_step == 2:
                        # Move Complete
                        game.pegs[to_peg].append(animating_disk)
                        game.move_count += 1
                        game._update_disk_positions()
                        animating_disk = None
                        
                        # Trigger move sound for AI moves
                        renderer.play_sound('move')
                        
                        if not ai_moves:
                            is_ai_running = False
                            # AI solve complete sound
                            renderer.play_sound('success')
                            puzzle_solved_played = True

            renderer.draw_game(game, is_ai_running, animating_disk)
            
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
