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

    CannonBall_IMG = None

    @classmethod
    def load_images(cls):
        if cls.CannonBall_IMG is None:
            cls.CannonBall_IMG = pygame.image.load(
                "assets/Cannon_ball.png"
            ).convert_alpha()


    def __init__(self, x, y, velocity, owner):
        super().__init__(x, y, 16, 16)
        CannonBall.load_images()
        self.vel = pygame.Vector2(velocity)
        self.owner = owner


        self.image = pygame.transform.scale(
            CannonBall.CannonBall_IMG,(16, 16)
        )

    def update(self, dt):
        self.rect.x += int(self.vel.x * dt)
        self.rect.y += int(self.vel.y * dt)

    def draw(self, surface, cam):
        pos = (self.rect.x - cam[0], self.rect.y - cam[1])
        surface.blit(self.image, pos)

    def draw(self, surface, cam):
        pos = (self.rect.x - cam[0], self.rect.y - cam[1])
        surface.blit(self.image, pos)




class Cannon(Entity):
    """
    Solid entity that periodically fires cannonballs.
    """

    CANNON_IMG = None

    @classmethod
    def load_images(cls):
        if cls.CANNON_IMG is None:
            cls.CANNON_IMG = pygame.image.load(
                "assets/cannon.png"
            ).convert_alpha()

    def __init__(self, x, y, direction, speed=220, interval=1.5):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)

        Cannon.load_images()

        self.dir = pygame.Vector2(DIRS[direction])
        self.speed = speed
        self.interval = interval
        self.timer = interval

        # scale sprite to tile
        self.image = pygame.transform.scale(
            Cannon.CANNON_IMG,
            (TILE_SIZE, TILE_SIZE)
        )

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

    # -------------------------
    # DRAW (SPRITE-BASED)
    # -------------------------
    def draw(self, surface, cam):
        # determine rotation angle
        if self.dir == pygame.Vector2(1, 0):      # right
            angle = 0
        elif self.dir == pygame.Vector2(0, 1):    # down
            angle = -90
        elif self.dir == pygame.Vector2(-1, 0):   # left
            angle = 180
        elif self.dir == pygame.Vector2(0, -1):   # up
            angle = 90
        else:
            angle = 0

        rotated = pygame.transform.rotate(self.image, angle)

        # keep center alignment after rotation
        rect = rotated.get_rect(center=self.rect.center)

        surface.blit(
            rotated,
            (
                rect.x - cam[0],
                rect.y - cam[1]
            )
        )
