import pygame
from constant import *
from logic import get_backup, restore_backup, generate_tiles, move_tiles, check_game_over, get_high_score, save_high_score

window = pygame.display.set_mode((width, height + ui_height)) 
pygame.display.set_caption("2048 UIT - Project")

def draw_interface(window, undo_rect, restart_rect, status, score, high_score):
    # 1. Vẽ nền cho khu vực UI phía dưới
    pygame.draw.rect(window, (250, 248, 239), (0, height, width, ui_height))
    
    # 2. Vẽ điểm số (Score)
    score_text = font_small.render(f"SCORE: {score}", True, font_color)
    high_score_text = font_small.render(f"BEST: {high_score}", True, font_color)
    window.blit(score_text, (20, height + (ui_height/2 - score_text.get_height()/2)))
    window.blit(high_score_text, (20, height + (ui_height/2 - high_score_text.get_height()/2) + 30))

    # 3. Vẽ nút Undo
    pygame.draw.rect(window, undo_btn_color, undo_rect, border_radius=8)
    undo_text = font_small.render("UNDO", True, (255, 255, 255))
    window.blit(undo_text, (undo_rect.x + (undo_rect.width/2 - undo_text.get_width()/2), 
                           undo_rect.y + (undo_rect.height/2 - undo_text.get_height()/2)))

    # 4. Vẽ nút Restart
    pygame.draw.rect(window, (242, 177, 121), restart_rect, border_radius=8)
    restart_text = font_small.render("RESTART", True, (255, 255, 255))
    window.blit(restart_text, (restart_rect.x + (restart_rect.width/2 - restart_text.get_width()/2), 
                              restart_rect.y + (restart_rect.height/2 - restart_text.get_height()/2)))

    # 5. Lớp phủ khi Thắng/Thua
    if status != "playing":
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        color = (237, 194, 46, 150) if status == "win" else (119, 110, 101, 150)
        overlay.fill(color)
        window.blit(overlay, (0, 0))
        
        msg = "YOU WIN!" if status == "win" else "GAME OVER!"
        result_text = font.render(msg, True, (255, 255, 255))
        window.blit(result_text, (width//2 - result_text.get_width()//2, height//2))
def draw_grid(window):
    """Vẽ lưới ngăn cách các ô."""
    for row in range(1, rows):
        y = row * rect_height
        pygame.draw.line(window, outline_color, (0, y), (width, y), outline_thickness)
    for col in range(1, cols):
        x = col * rect_width
        pygame.draw.line(window, outline_color, (x, 0), (x, height), outline_thickness)
    pygame.draw.rect(window, outline_color, (0, 0, width, height), outline_thickness)

def draw_all(window, tiles, undo_rect, restart_rect, status, score, high_score):
    window.fill(background_color) 
    
    for tile in tiles.values():
        tile.draw(window)
        
    draw_grid(window)           
    
    # TRUYỀN ĐÚNG THỨ TỰ VÀO ĐÂY:
    draw_interface(window, undo_rect, restart_rect, status, score, high_score) 
    
    pygame.display.update()
def main(window):
    clock = pygame.time.Clock() 
    tiles = generate_tiles() 
    undo_stack = []      
    status = "playing"   
    score = 0 
    high_score = get_high_score() 
    
    undo_rect = pygame.Rect(width // 2 - 60, height + 25, 120, 50)
    restart_rect = pygame.Rect(width // 2 + 80, height + 25, 150, 50)

    run = True 
    while run:
        clock.tick(fps)
        draw_all(window, tiles, undo_rect, restart_rect, status, score, high_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    tiles = generate_tiles()
                    undo_stack.clear()
                    score = 0
                    status = "playing"
                
                elif undo_rect.collidepoint(event.pos):
                    if undo_stack:
                        backup_data, prev_score = undo_stack.pop()
                        tiles = restore_backup(backup_data)
                        score = prev_score 
                        status = check_game_over(tiles)

            if status == "playing":
                if event.type == pygame.KEYDOWN:
                    direction = None
                    if event.key == pygame.K_LEFT: direction = "left"
                    elif event.key == pygame.K_RIGHT: direction = "right"
                    elif event.key == pygame.K_UP: direction = "up"
                    elif event.key == pygame.K_DOWN: direction = "down"

                    if direction:
                        undo_stack.append((get_backup(tiles), score))
                        if len(undo_stack) > 20: undo_stack.pop(0)

                        gained, moved = move_tiles(window, tiles, clock, direction, lambda w, t: draw_all(w, t, undo_rect, restart_rect, status, score, high_score))
                        
                        if moved:
                            score += gained
                        else:
                            undo_stack.pop()

                        if score > high_score:
                            high_score = score
                            save_high_score(high_score)
                        
                        status = check_game_over(tiles)
                    
                    if event.key == pygame.K_u:
                        if undo_stack:
                            backup_data, prev_score = undo_stack.pop()
                            tiles = restore_backup(backup_data)
                            score = prev_score
                            status = check_game_over(tiles)

    pygame.quit()
if __name__ == "__main__":
    main(window)