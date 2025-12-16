import pygame
from core.entity import Entity
from settings import TILE_SIZE, GRAVITY


class Goblin(Entity):
    def __init__(self, x, y, sprites, speed=1.4):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.sprites = sprites
        self.frame = 0
        self.anim_timer = 0.0

        self.vel = pygame.Vector2(speed, 0)
        self.speed = speed
        self.on_ground = False
        self.facing = 1  # 1 = right, -1 = left

    def update(self, dt, solids):
        # gravity
        self.vel.y += GRAVITY

        # -----------------
        # horizontal
        self.rect.x += int(self.vel.x)

        hit_wall = False
        for s in solids:
            if self.rect.colliderect(s.rect):
                if self.vel.x > 0:
                    self.rect.right = s.rect.left
                else:
                    self.rect.left = s.rect.right
                hit_wall = True

        if hit_wall:
            self.vel.x *= -1
            self.facing *= -1

        # -----------------
        # vertical
        self.on_ground = False
        self.rect.y += int(self.vel.y)

        for s in solids:
            if self.rect.colliderect(s.rect):
                if self.vel.y > 0:
                    self.rect.bottom = s.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = s.rect.bottom
                    self.vel.y = 0

        # -----------------
        # animation
        self.anim_timer += dt
        if self.anim_timer >= 0.15:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(self.sprites)

    def draw(self, surface, cam):
        img = self.sprites[self.frame]
        if self.facing < 0:
            img = pygame.transform.flip(img, True, False)

        # 🔑 visual offset (lower sprite, keep hitbox correct)
        SPRITE_Y_OFFSET = 4

        surface.blit(
            img,
            (self.rect.x - cam[0], self.rect.y - cam[1] + SPRITE_Y_OFFSET)
        )

