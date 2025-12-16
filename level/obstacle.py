import pygame
from core.entity import Entity
from settings import TILE_SIZE, GRAVITY


class PushBlock(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.vel = pygame.Vector2(0, 0)
        self.grabbed = False

    def update(self, solids):
        # -------------------------
        # GRAVITY
        # -------------------------
        self.vel.y += GRAVITY

        # -------------------------
        # VERTICAL MOVE
        # -------------------------
        self.rect.y += int(self.vel.y)

        for s in solids:
            if self.rect.colliderect(s.rect):
                if self.vel.y > 0:
                    self.rect.bottom = s.rect.top
                    self.vel.y = 0
                elif self.vel.y < 0:
                    self.rect.top = s.rect.bottom
                    self.vel.y = 0

        # -------------------------
        # HORIZONTAL MOVE
        # (velocity is set by merged player)
        # -------------------------
        self.rect.x += int(self.vel.x)

        for s in solids:
            # 🔑 only block sideways movement if overlapping vertically
            if self.rect.bottom > s.rect.top and self.rect.top < s.rect.bottom:
                if self.rect.colliderect(s.rect):
                    if self.vel.x > 0:
                        self.rect.right = s.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = s.rect.right

        # Reset horizontal velocity each frame
        self.vel.x = 0

    def draw(self, surface, cam):
        r = self.rect.move(-cam[0], -cam[1])
        pygame.draw.rect(surface, (120, 110, 100), r)
        pygame.draw.rect(surface, (40, 30, 20), r, 2)
