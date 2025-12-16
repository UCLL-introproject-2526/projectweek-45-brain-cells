import pygame
from core.entity import Entity
from settings import TILE_SIZE

class Switch(Entity):
    """
    On when a player or block is standing on it.
    """
    def __init__(self, x, y, w=48, h=12, key="A"):
        super().__init__(x, y, w, h)
        self.key = key
        self.on = False

    def update(self, dt, actors):
        self.on = False
        for a in actors:
            feet = pygame.Rect(
                a.rect.left + 6,
                a.rect.bottom - 4,
                a.rect.width - 12,
                6
            )
            if feet.colliderect(self.rect):
                self.on = True
                break

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        color = (60, 210, 90) if self.on else (170, 60, 60)
        pygame.draw.rect(surface, color, r)
        pygame.draw.rect(surface, (20, 20, 20), r, 2)


class Door:
    def __init__(self, x, y, w, h, key, mode="hold", logic="AND"):
        self.rect = pygame.Rect(x, y, w, h)
        self.key = key
        self.mode = mode        # "hold" or "latch" (kept for compatibility)
        self.logic = logic      # "AND" or "OR"
        self.open = False

    @property
    def solid(self):
        return not self.open

    def update(self, plates):
        linked = [p for p in plates if p.key == self.key]
        if not linked:
            return

        if self.logic == "AND":
            self.open = all(p.active for p in linked)

        elif self.logic == "OR":
            self.open = any(p.active for p in linked)

    def draw(self, surface, cam):
        if self.open:
            return

        r = self.rect.move(-cam[0], -cam[1])
        pygame.draw.rect(surface, (60, 60, 80), r)




class Finish(Entity):
    def __init__(self, x, y, w=64, h=96):
        super().__init__(x, y, w, h)

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, (220, 220, 255), r, 2)
        pygame.draw.line(
            surface,
            (220, 220, 255),
            (r.centerx, r.top),
            (r.centerx, r.bottom),
            2
        )


class PressurePlate:
    def __init__(self, x, y, key):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE/4)
        self.key = key
        self.active = False

    def update(self, actors):
        self.active = any(self.rect.colliderect(a.rect) for a in actors)

    def draw(self, surface, cam):
        r = self.rect.move(-cam[0], -cam[1])
        color = (200, 80, 80) if self.active else (120, 40, 40)
        pygame.draw.rect(surface, color, r)



class LatchPlate(PressurePlate):
    def __init__(self, x, y, key):
        super().__init__(x, y, key)
        self.triggered = False

    def update(self, actors):
        if not self.triggered:
            super().update(actors)
            if self.active:
                self.triggered = True
                self.active = True
        else:
            self.active = True


class HoldPlate(PressurePlate):
    pass
