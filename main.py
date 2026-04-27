import pygame
from constant import *
from logic import get_backup, restore_backup, generate_tiles, move_tiles, check_game_over

window = pygame.display.set_mode((width, height + ui_height)) 
pygame.display.set_caption("2048 UIT - Project")

def draw_interface(window, undo_rect, restart_rect, status, score):
    # 1. Vẽ nền cho khu vực UI phía dưới
    pygame.draw.rect(window, (250, 248, 239), (0, height, width, ui_height))
    
    # 2. Vẽ điểm số (Score)
    score_text = font_small.render(f"SCORE: {score}", True, font_color)
    window.blit(score_text, (20, height + (ui_height/2 - score_text.get_height()/2)))

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

def draw_all(window, tiles, undo_rect, restart_rect, status, score):
    window.fill(background_color) 
    
    for tile in tiles.values():
        tile.draw(window)
        
    draw_grid(window)           
    
    # TRUYỀN ĐÚNG THỨ TỰ VÀO ĐÂY:
    draw_interface(window, undo_rect, restart_rect, status, score) 
    
    pygame.display.update()
def main(window):
    clock = pygame.time.Clock() 
    tiles = generate_tiles() 
    undo_stack = []      
    status = "playing"   
    score = 0 # <--- Khởi tạo biến điểm số
    
    # Định nghĩa vị trí 2 nút bấm (Căn giữa và lệch nhau 1 chút)
    undo_rect = pygame.Rect(width // 2 - 60, height + 25, 120, 50)
    restart_rect = pygame.Rect(width // 2 + 80, height + 25, 150, 50)

    run = True 
    while run:
        clock.tick(fps)
        draw_all(window, tiles, undo_rect, restart_rect, status, score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                break

            # Bấm chuột (Cho phép bấm Restart hoặc Undo ngay cả khi đã Game Over)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    # CHƠI LẠI: Reset toàn bộ game
                    tiles = generate_tiles()
                    undo_stack.clear()
                    score = 0
                    status = "playing"
                
                elif undo_rect.collidepoint(event.pos):
                    if undo_stack:
                        # Rút cả bảng tiles và score cũ ra khỏi Stack
                        backup_data, prev_score = undo_stack.pop()
                        tiles = restore_backup(backup_data)
                        score = prev_score # Trả lại điểm cũ
                        status = check_game_over(tiles) # Cập nhật lại status (lỡ đang Game Over mà Undo thì cho chơi tiếp)

            # Xử lý khi game đang chơi
            if status == "playing":
                if event.type == pygame.KEYDOWN:
                    direction = None
                    if event.key == pygame.K_LEFT: direction = "left"
                    elif event.key == pygame.K_RIGHT: direction = "right"
                    elif event.key == pygame.K_UP: direction = "up"
                    elif event.key == pygame.K_DOWN: direction = "down"

                    if direction:
                        # PUSH VÀO STACK: Lưu lại trạng thái Bảng và Điểm hiện tại
                        undo_stack.append((get_backup(tiles), score))
                        if len(undo_stack) > 20: undo_stack.pop(0)
                        
                        # Di chuyển và nhận số điểm cộng thêm
                        gained = move_tiles(window, tiles, clock, direction, lambda w, t: draw_all(w, t, undo_rect, restart_rect, status, score))
                        score += gained # Cộng điểm
                        
                        status = check_game_over(tiles)
                    
                    # Phím tắt U để Undo
                    if event.key == pygame.K_u:
                        if undo_stack:
                            backup_data, prev_score = undo_stack.pop()
                            tiles = restore_backup(backup_data)
                            score = prev_score
                            status = check_game_over(tiles)

    pygame.quit()
if __name__ == "__main__":
    main(window)