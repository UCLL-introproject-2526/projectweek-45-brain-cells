import pygame
from settings import GRAVITY

class PhysicsBody:
    def __init__(self):
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False

    def apply_gravity(self):
        self.vel.y += GRAVITY

    def _resolve_vs_solids(self, rect, solids):
        # solids must have .rect
        for s in solids:
            if rect.colliderect(s.rect):
                yield s

    def move_and_collide(self, rect, solids, dt=0.0):
        # Horizontal
        rect.x += int(self.vel.x)
        for s in self._resolve_vs_solids(rect, solids):
            if self.vel.x > 0:
                rect.right = s.rect.left
            elif self.vel.x < 0:
                rect.left = s.rect.right
            self.vel.x = 0

        # Vertical
        rect.y += int(self.vel.y)
        self.on_ground = False
        for s in self._resolve_vs_solids(rect, solids):
            if self.vel.y > 0:
                rect.bottom = s.rect.top
                self.on_ground = True
            elif self.vel.y < 0:
                rect.top = s.rect.bottom
            self.vel.y = 0
