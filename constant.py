import pygame

pygame.init()

fps = 60
width, height = 800, 800
ui_height = 100
rows = 4
cols = 4
rect_height = height // rows
rect_width = width // cols
outline_thickness = 10 
move_vel = 20 

outline_color = (187, 173, 160) 
background_color = (205, 192, 180)
font_color = (119, 110, 101) 
undo_btn_color = (143, 122, 102) # Màu nút Undo
win_overlay = (237, 194, 46, 150) # Vàng trong suốt
lose_overlay = (119, 110, 101, 150) # Xám trong suốt

font = pygame.font.SysFont("comicsansms", 40, bold=True)
font_small = pygame.font.SysFont("comicsansms", 25, bold=True)



