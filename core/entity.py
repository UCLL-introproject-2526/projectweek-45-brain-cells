import pygame

class Entity:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def update(self, dt, *args, **kwargs):
        pass

    def draw(self, surface, camera_offset=(0, 0)):
        pygame.draw.rect(surface, (200, 50, 50), self.rect.move(-camera_offset[0], -camera_offset[1]))
