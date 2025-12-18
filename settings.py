import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

MENU_MUSIC = "assets/music/main_menu.mp3"
GAME_MUSIC = "assets/music/level_music.mp3"



TILE_SIZE = 45
GRAVITY = 0.85

GRAB_KEY = pygame.K_LSHIFT
GRAB_RANGE = 12


# Player physics
PLAYER_W, PLAYER_H = (2/3)*TILE_SIZE, TILE_SIZE
PLAYER_SPEED = 4.2
PLAYER_JUMP = -14

# Merged physics
MERGED_W, MERGED_H = PLAYER_W*1.625 , 1.41666*PLAYER_H 
MERGED_SPEED = 3.4
MERGED_JUMP = -18

# Merge rules
MERGE_DISTANCE = 1.2*TILE_SIZE
MERGE_COOLDOWN_SEC = 0.20

# Block physics
BLOCK_FRICTION = 0.86
BLOCK_MAX_SPEED = 7.5

# Death
KILL_Y = 9000 #Falling below this kills the player

# Colors
BG = (15, 15, 22)
STONE = (70, 70, 80)
STONE_DARK = (45, 45, 55)
TORCH_GLOW = (255, 160, 40)
