import pygame
from settings import TILE_SIZE


def load_goblin_sprites():
    frames = []
    for i in range(4):
        img = pygame.image.load(f"assets/goblin/{i+1}.png").convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        frames.append(img)
    return frames
