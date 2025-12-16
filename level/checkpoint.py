import pygame
from core.entity import Entity
from settings import TILE_SIZE


class Checkpoint(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.active = False

    def try_activate(self, merged, level):
        """
        Activate checkpoint ONLY when merged entity touches it.
        Updates respawn positions for split players.
        """
        if self.active:
            return
        if merged and self.rect.colliderect(merged.rect):
            self.active = True

            level.respawn_p1 = (self.rect.centerx - 40, self.rect.bottom - 48)
            level.respawn_p2 = (self.rect.centerx + 40, self.rect.bottom - 48)

    def draw(self, surface, cam):
        r = self.rect.move(-cam[0], -cam[1])
        color = (80, 200, 120) if self.active else (60, 60, 60)
        pygame.draw.rect(surface, color, r)
        pygame.draw.rect(surface, (20, 20, 20), r, 2)
