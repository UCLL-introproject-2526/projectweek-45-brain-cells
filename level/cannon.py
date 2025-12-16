import pygame
from core.entity import Entity
from settings import TILE_SIZE

DIRS = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


class CannonBall(Entity):
    def __init__(self, x, y, velocity, owner):
        super().__init__(x, y, 16, 16)
        self.vel = pygame.Vector2(velocity)
        self.owner = owner

    def update(self, dt):
        self.rect.x += int(self.vel.x * dt)
        self.rect.y += int(self.vel.y * dt)

    def draw(self, surface, cam):
        r = self.rect.move(-cam[0], -cam[1])
        pygame.draw.circle(surface, (40, 40, 40), r.center, 8)
        pygame.draw.circle(surface, (140, 140, 140), r.center, 8, 2)


class Cannon(Entity):
    """
    Solid entity that periodically fires cannonballs.
    """
    def __init__(self, x, y, direction, speed=220, interval=1.5):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.dir = pygame.Vector2(DIRS[direction])
        self.speed = speed
        self.interval = interval
        self.timer = interval

    def update(self, dt, level):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.interval
            self.fire(level)

    def fire(self, level):
        # spawn OUTSIDE the cannon barrel
        offset = self.dir * (TILE_SIZE // 2 + 8)

        cx = self.rect.centerx + offset.x - 8
        cy = self.rect.centery + offset.y - 8

        vx = self.dir.x * self.speed
        vy = self.dir.y * self.speed

        level.cannonballs.append(
            CannonBall(cx, cy, (vx, vy), owner=self)
    )


    def draw(self, surface, cam):
        r = self.rect.move(-cam[0], -cam[1])
        pygame.draw.rect(surface, (90, 90, 90), r)
        barrel = (
            r.centerx + int(self.dir.x * 12),
            r.centery + int(self.dir.y * 12),
        )
        pygame.draw.circle(surface, (40, 40, 40), barrel, 6)
