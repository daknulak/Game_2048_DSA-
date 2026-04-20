import random
import math
import pygame
from constant import * 
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
        self.value = value
        self.row = row
        self.col = col
        #toạ độ x, y
        self.x = col * rect_width
        self.y = row * rect_height
    
    def get_color(self):
        """
        Tính toán màu sắc dựa trên giá trị của ô số.
        Sử dụng hàm logarit cơ số 2 để tìm chỉ số màu
        """
        color_index = int(math.log2(self.value)) - 1
        return self.colors[min(color_index, len(self.colors) - 1)]

    def draw(self, window):
        """
        Vẽ ô số và giá trị của nó lên màn hình
        """
        color = self.get_color()
        #vẽ hình vuông nền của ô số
        pygame.draw.rect(window, color, (self.x, self.y, rect_width, rect_height)) 
        text = font.render(str(self.value), 1, font_color) 
        #tính toán căn giữa chữ vào trong ô số
        window.blit(text, (self.x + (rect_width/2 - text.get_width()/2), 
                           self.y + (rect_height/2 - text.get_height()/2)))

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
    """
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

def end_move(tiles):
    """
    Kiểm tra thua cuộc và sinh ô số mới (2 hoặc 4)
    """
    if len(tiles) == 16:
        return "lost"
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"

def move_tiles(window, tiles, clock, direction, draw_func):
    """
    Xử lý logic di chuyển, va chạm và gộp cho các ô số
    Sử dụng kỹ thuật Functional Programming (Lambda) để xử lý đa hướng
    """
    updated = True
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-move_vel, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + move_vel
        move_check = lambda tile, next_tile: tile.x > next_tile.x + rect_width + move_vel
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (move_vel, 0)
        boundary_check = lambda tile: tile.col == cols - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - move_vel
        move_check = lambda tile, next_tile: tile.x + rect_width + move_vel < next_tile.x
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -move_vel)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + move_vel
        move_check = lambda tile, next_tile: tile.y > next_tile.y + rect_height + move_vel
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, move_vel)
        boundary_check = lambda tile: tile.row == rows - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - move_vel
        move_check = lambda tile, next_tile: tile.y + rect_height + move_vel < next_tile.y
        ceil = False

    while updated:
        clock.tick(fps)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile): continue
            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else: continue
            tile.set_pos(ceil)
            updated = True
        update_tiles(window, tiles, sorted_tiles)
        draw_func(window, tiles)
    return end_move(tiles)

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