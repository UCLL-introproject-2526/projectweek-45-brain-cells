import pygame
from core.entity import Entity

class Spike(Entity):
    def __init__(self, x, y, w=48, h=24):
        super().__init__(x, y, w, h)

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        points = [
            (r.left, r.bottom),
            (r.centerx - 12, r.top),
            (r.centerx, r.bottom),
            (r.centerx + 12, r.top),
            (r.right, r.bottom)
        ]
        pygame.draw.polygon(surface, (180, 180, 190), points)
        pygame.draw.polygon(surface, (40, 40, 45), points, 2)
