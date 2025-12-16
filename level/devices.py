import pygame
from core.entity import Entity


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


class Door(Entity):
    """
    Solid when closed; non-solid when open.
    Has a cooldown so it doesn't snap shut immediately.
    """
    def __init__(self, x, y, w=48, h=96, requires=None, cooldown=1.5):
        super().__init__(x, y, w, h)
        self.requires = requires or []
        self.cooldown = cooldown
        self.timer = 0.0
        self.open = False

    @property
    def solid(self):
        return not self.open

    def update(self, dt):
        if all(s.on for s in self.requires):
            self.timer = self.cooldown
        else:
            self.timer = max(0.0, self.timer - dt)

        self.open = self.timer > 0.0

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        if self.open:
            pygame.draw.rect(surface, (40, 40, 60), r, 2)
        else:
            pygame.draw.rect(surface, (80, 60, 120), r)
            pygame.draw.rect(surface, (20, 20, 20), r, 3)


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
