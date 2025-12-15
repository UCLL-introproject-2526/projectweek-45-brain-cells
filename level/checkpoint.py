import pygame
from core.entity import Entity

class Checkpoint(Entity):
    def __init__(self, x, y, w=32, h=48):
        super().__init__(x, y, w, h)
        self.activated = False

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        col = (90, 220, 140) if self.activated else (70, 120, 90)
        pygame.draw.rect(surface, col, r, border_radius=6)
        pygame.draw.rect(surface, (10, 10, 10), r, 2, border_radius=6)
