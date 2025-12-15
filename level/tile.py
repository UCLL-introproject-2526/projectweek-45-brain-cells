import pygame
from core.entity import Entity
from settings import STONE, STONE_DARK

class Tile(Entity):
    def __init__(self, x, y, size, variant=0):
        super().__init__(x, y, size, size)
        self.variant = variant

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, STONE if self.variant == 0 else STONE_DARK, r)
        pygame.draw.rect(surface, (20, 20, 25), r, 2)
