import os
import random
import math
import pygame
from constant import * 
def get_save_path():
    """Xác định đường dẫn lưu trữ điểm cao (high score) trên máy người dùng"""
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, "high_score_2048.txt")
class Tile:
    """
    Đại diện cho một ô số (Square) trên bàn chơi.
    Quản lý giá trị, tọa độ đồ họa và các phương thức hiển thị/di chuyển.
    """
    #Bảng màu đại diện cho các giá trị từ 2 đến 2048+
    colors = [
        (238, 228, 218), (237, 224, 200), (242, 177, 121),
        (245, 149, 99), (246, 124, 95), (246, 94, 59),
        (237, 207, 114), (237, 204, 97), (237, 200, 80),
        (237, 197, 63), (237, 194, 46), (60, 58, 50), (30, 30, 30),
    ]

    def __init__(self, value, row, col):
        """
        Khởi tạo một ô số mới.
        
        Args:
            value (int): Giá trị của ô (2, 4, 8,...).
            row (int): Chỉ số hàng trong ma trận (0-3).
            col (int): Chỉ số cột trong ma trận (0-3).
        """
        self.scale = 1.0
        self.value = value
        self.row = row
        self.col = col
        #toạ độ x, y
        self.x = col * rect_width
        self.y = row * rect_height
    def play_pop_animation(self):
        """Kích hoạt hiệu ứng nảy lên"""
        self.scale = 1.2
    def get_color(self):
        """
        Tính toán màu sắc dựa trên giá trị của ô số.
        Sử dụng hàm logarit cơ số 2 để tìm chỉ số màu
        """
        color_index = int(math.log2(self.value)) - 1
        return self.colors[min(color_index, len(self.colors) - 1)]

    def draw(self, window):
        """
        Vẽ ô số và giá trị của nó lên màn hình (Có kèm hiệu ứng Pop-up)
        """
        # Kiểm tra xem biến scale đã có chưa (đề phòng bạn quên khởi tạo ở __init__)
        if not hasattr(self, 'scale'):
            self.scale = 1.0
            
        if self.scale > 1.0:
            self.scale -= 0.05  # Tốc độ giảm xuống 
            if self.scale < 1.0:
                self.scale = 1.0

        #TÍNH KÍCH THƯỚC MỚI SAU KHI PHÓNG TO 
        current_w = rect_width * self.scale
        current_h = rect_height * self.scale

        #TÍNH TOẠ ĐỘ VẼ (Tính từ tâm để phóng to đều ra xung quanh)
        center_x = self.x + (rect_width / 2)
        center_y = self.y + (rect_height / 2)
        
        draw_x = center_x - (current_w / 2)
        draw_y = center_y - (current_h / 2)

        color = self.get_color()
        
        #VẼ HÌNH VUÔNG NỀN (Dùng kích thước và tọa độ mới)
        pygame.draw.rect(window, color, (draw_x, draw_y, current_w, current_h), border_radius=5) 
        
        #vẽ chữ số
        text = font.render(str(self.value), 1, font_color) 
        
        text = pygame.transform.smoothscale(text, (int(text.get_width() * self.scale), int(text.get_height() * self.scale)))
        
        # Căn giữa chữ dựa trên toạ độ trung tâm đã tính
        window.blit(text, (center_x - text.get_width() / 2, 
                           center_y - text.get_height() / 2))

    def set_pos(self, ceil=False):
        """
        Cập nhật lại vị trí hàng và cột dựa trên toạ độ pixel hiện tại.
        Thường dùng sau khi kết thúc quá trình animation di chuyển
        """
        if ceil:
            self.row = math.ceil(self.y / rect_height)
            self.col = math.ceil(self.x / rect_width) 
        else:
            self.row = math.floor(self.y / rect_height)
            self.col = math.floor(self.x / rect_width) 

    def move(self, delta):
        """
        Dịch chuyển toạ độ pixel của các ô số
        Args:
            delta (tuple): Khoảng dịch chuyển (dx, dy).
        """
        self.x += delta[0]
        self.y += delta[1] 

def get_backup(tiles):
    """
    Sao lưu trạng thái hiện tại để đẩy vào Stack (phục vụ tính năng Undo)
    Lưu trữ dưới dạng Dict chứa dữ liệu thô (Raw data)
    """
    return {key: (tile.value, tile.row, tile.col) for key, tile in tiles.items()}

def restore_backup(backup_data):
    """
    Khôi phục trạng thái từ dữ liệu sao lưu
    Tải cấu trúc của class Tile từ dữ liệu thô
    """
    return {key: Tile(val, r, c) for key, (val, r, c) in backup_data.items()} 

def get_random_pos(tiles):
    """
    Tìm kiếm một vị trí ngẫu nhiên còn trống
    """
    while True:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        if f"{row}{col}" not in tiles:
            return row, col

def generate_tiles(): 
    """
    Khởi tạo trạng thái ban đầu của game với 2 ô số 2
    """
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col) 
    return tiles

def update_tiles(window, tiles, sorted_tiles):
    """
    Đồng bộ hoá Dict 'tiles' dựa trên danh sách các ô số đã thay đổi vị trí
    Args:
        window: màn hình hiển hiển thị
        tiles (dict): bàn cờ hiện tại cần được cập nhật
        sorted_tiles (list): danh sách các ô số đã được sắp xếp lại sau khi trượt
    """
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

def end_move(tiles):
    """
    Kiểm tra thua cuộc và sinh ô số mới (2 hoặc 4)
    Args:
        tiles (dict): bàn cờ hiện tại
    Returns:
        str: 'lost' nếu bảng đã đầy 16 ô, ngược lại trở về 'continue'
    """
    if len(tiles) == 16:
        return "lost"
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"

def move_tiles(window, tiles, clock, direction, draw_func):
    """Xử lý logic dịch chuyển và gộp các ô số theo hướng chỉ định
    Args:
        window: Cửa sổ game để vẽ lại sau mỗi bước di chuyển
        tiles: Dict chứa tất cả các ô số hiện tại trên bàn chơi
        clock: Đồng hồ để kiểm soát tốc độ animation
        direction: Hướng di chuyển ("left", "right", "up", "down")
        draw_func: Hàm vẽ lại bàn chơi sau mỗi bước di chuyển
    Returns:
        score_gained: Điểm số thu được sau bước di chuyển (từ việc gộp các ô số)
        board_changed: Boolean cho biết liệu có sự thay đổi nào trên bàn chơi hay không (để quyết định có nên sinh ô số mới hay không)
    """
    updated = True
    blocks = set()
    score_gained = 0
    board_changed = False

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-move_vel, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + move_vel
        move_check = lambda tile, next_tile: tile.x > next_tile.x + rect_width
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (move_vel, 0)
        boundary_check = lambda tile: tile.col == cols - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - move_vel
        move_check = lambda tile, next_tile: tile.x + rect_width < next_tile.x
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -move_vel)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + move_vel
        move_check = lambda tile, next_tile: tile.y > next_tile.y + rect_height
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, move_vel)
        boundary_check = lambda tile: tile.row == rows - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - move_vel
        move_check = lambda tile, next_tile: tile.y + rect_height < next_tile.y
        ceil = False

    while updated:
        clock.tick(fps)
        updated = False
        
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)
        to_remove = []

        for tile in sorted_tiles:
            if boundary_check(tile): continue
            
            next_tile = get_next_tile(tile)
            
            if not next_tile:
                tile.move(delta)
                updated = True
                board_changed = True
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile, next_tile):
                    tile.move(delta)
                    updated = True
                    board_changed = True
                else:
                    tile.move(delta) 
                    next_tile.value *= 2
                    score_gained += next_tile.value
                    next_tile.play_pop_animation()
                    
                    blocks.add(next_tile)
                    to_remove.append(tile)
                    updated = True
                    board_changed = True
            elif move_check(tile, next_tile):
                tile.move(delta)
                updated = True
                board_changed = True
            else:
                continue
            
            tile.set_pos(ceil)

        new_tiles = {}
        for t in sorted_tiles:
            if t not in to_remove:
                new_tiles[f"{t.row}{t.col}"] = t
        
        tiles.clear()
        tiles.update(new_tiles)

        draw_func(window, tiles)

    if board_changed:
        end_move(tiles)
        
    return score_gained, board_changed
def check_game_over(tiles):
    """
    Kiểm tra trạng thái game.
    Returns: "win", "lose", hoặc "playing"
    """
    for tile in tiles.values():
        if tile.value == 2048:
            return "win"

    if len(tiles) < 16:
        return "playing"

    for r in range(rows):
        for c in range(cols):
            current_val = tiles.get(f"{r}{c}").value
            right = tiles.get(f"{r}{c+1}")
            down = tiles.get(f"{r+1}{c}")
            
            if (right and right.value == current_val) or (down and down.value == current_val):
                return "playing"

    return "lose"

def get_high_score():
    """
    Đọc điểm cao nhất đã lưu từ file. Nếu file không tồn tại hoặc có lỗi, trả về 0.
    """ 
    try:
        path = get_save_path()
        # Kiểm tra xem file có tồn tại không trước khi mở
        if not os.path.exists(path):
            return 0
            
        with open(path, "r") as f:
            content = f.read().strip()
            if content:
                return int(content)
            return 0 # Nếu file trống thì trả về 0
    except Exception:
        # Nếu có bất kỳ lỗi gì (đọc file, ép kiểu...), mặc định trả về 0
        return 0
def save_high_score(score):
    """Lưu trữ điểm cao nhất vào file"""
    try:
        with open(get_save_path(), "w") as f:
            f.write(str(score))
    except Exception:
        pass