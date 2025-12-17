import pygame


class Camera:
    """
    Simple 2D camera storing world offset.
    """
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)

    def move(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy

    def apply(self, world_pos):
        return world_pos - self.pos

    def screen_to_world(self, screen_pos):
        return screen_pos + self.pos
