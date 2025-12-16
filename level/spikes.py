import pygame
from core.entity import Entity
from settings import TILE_SIZE

class Spike(Entity):
    def __init__(self, x, y, w=TILE_SIZE, h=TILE_SIZE):
        super().__init__(x, y, w, h)

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])

        # A single triangle
        points = [
            (r.left, r.bottom),      # bottom-left
            (r.centerx, r.top),      # top
            (r.right, r.bottom)      # bottom-right
        ]

        pygame.draw.polygon(surface, (180, 180, 190), points)
