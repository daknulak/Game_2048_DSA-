import pygame
from constant import *
from logic import get_backup, restore_backup, generate_tiles, move_tiles, check_game_over

# Khởi tạo cửa sổ (chiều cao = bàn chơi + khu vực UI)
window = pygame.display.set_mode((width, height + ui_height)) 
pygame.display.set_caption("2048 UIT - Project")

def draw_interface(window, undo_rect, status):
    """Vẽ khu vực điều khiển và thông báo trạng thái game."""
    # 1. Vẽ nền cho khu vực UI phía dưới
    pygame.draw.rect(window, (250, 248, 239), (0, height, width, ui_height))
    
    # 2. Vẽ nút Undo
    pygame.draw.rect(window, undo_btn_color, undo_rect, border_radius=8)
    undo_text = font_small.render("UNDO (U)", True, (255, 255, 255))
    window.blit(undo_text, (undo_rect.x + (undo_rect.width/2 - undo_text.get_width()/2), 
                           undo_rect.y + (undo_rect.height/2 - undo_text.get_height()/2)))

    # 3. Nếu Thắng hoặc Thua, vẽ lớp phủ mờ (Overlay)
    if status != "playing":
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        # Màu vàng nếu thắng, màu xám nếu thua (độ trong suốt 150)
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

def draw_all(window, tiles, undo_rect, status):
    """Hàm tổng hợp để vẽ toàn bộ mọi thứ."""
    window.fill(background_color) 
    
    # Vẽ các ô số
    for tile in tiles.values():
        tile.draw(window)
        
    draw_grid(window)           # Vẽ lưới
    draw_interface(window, undo_rect, status) # Vẽ nút và thông báo
    
    pygame.display.update() 

def main(window):
    clock = pygame.time.Clock() 
    tiles = generate_tiles() 
    undo_stack = []      # Khởi tạo Stack lưu trữ các trạng thái
    status = "playing"   # Trạng thái ban đầu
    
    # Định nghĩa vùng nút Undo (Hình chữ nhật để bắt sự kiện Click)
    undo_rect = pygame.Rect(width // 2 - 75, height + 25, 150, 50)

    run = True 
    while run:
        clock.tick(fps)
        
        # Luôn vẽ lại màn hình ở mỗi vòng lặp
        draw_all(window, tiles, undo_rect, status)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                break

            # Xử lý khi game đang chơi
            if status == "playing":
                
                # 1. Bắt sự kiện Click chuột vào nút Undo
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if undo_rect.collidepoint(event.pos):
                        if undo_stack:
                            tiles = restore_backup(undo_stack.pop())

                # 2. Bắt sự kiện phím bấm
                if event.type == pygame.KEYDOWN:
                    direction = None
                    if event.key == pygame.K_LEFT: direction = "left"
                    elif event.key == pygame.K_RIGHT: direction = "right"
                    elif event.key == pygame.K_UP: direction = "up"
                    elif event.key == pygame.K_DOWN: direction = "down"

                    if direction:
                        # PUSH: Sao lưu trạng thái hiện tại vào Stack trước khi trượt
                        current_state = get_backup(tiles)
                        undo_stack.append(current_state)
                        
                        # Giới hạn Stack để không tốn ram (tối đa 20 bước)
                        if len(undo_stack) > 20: undo_stack.pop(0)
                        
                        # Thực hiện trượt và cộng dồn
                        move_tiles(window, tiles, clock, direction, lambda w, t: draw_all(w, t, undo_rect, status))
                        
                        # Cập nhật trạng thái Thắng/Thua sau mỗi nước đi
                        status = check_game_over(tiles)
                    
                    # Phím tắt U để Undo
                    if event.key == pygame.K_u:
                        if undo_stack:
                            tiles = restore_backup(undo_stack.pop())

    pygame.quit()

if __name__ == "__main__":
    main(window)