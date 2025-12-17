import pygame
from settings import GRAVITY, TILE_SIZE

class Goblin:
    def __init__(self, x, y, sprites):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.vel = pygame.Vector2(0, 0)
        self.sprites = sprites
        self.frame = 0
        self.anim_timer = 0

        self.speed = 1.4
        self.facing = 1  # 1 = right, -1 = left

    def update(self, dt, solids):
        # -------------------------
        # GRAVITY
        # -------------------------
        self.vel.y += GRAVITY
        self.rect.y += int(self.vel.y)

        for s in solids:
            if self.rect.colliderect(s.rect):
                if self.vel.y > 0:
                    self.rect.bottom = s.rect.top
                    self.vel.y = 0

        # -------------------------
        # EDGE DETECTION
        # -------------------------
        foot_x = self.rect.centerx + self.facing * (self.rect.width // 2 + 2)
        foot_y = self.rect.bottom + 2

        ground_ahead = False
        foot_rect = pygame.Rect(foot_x, foot_y, 2, 2)

        for s in solids:
            if foot_rect.colliderect(s.rect):
                ground_ahead = True
                break

        if not ground_ahead:
            self.facing *= -1

        # -------------------------
        # HORIZONTAL MOVE
        # -------------------------
        self.rect.x += int(self.speed * self.facing)

        for s in solids:
            if self.rect.colliderect(s.rect):
                if self.facing > 0:
                    self.rect.right = s.rect.left
                else:
                    self.rect.left = s.rect.right
                self.facing *= -1

        # -------------------------
        # ANIMATION
        # -------------------------
        self.anim_timer += dt
        if self.anim_timer > 0.15:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(self.sprites)


    def draw(self, surface, cam):
        img = self.sprites[self.frame]
        if self.facing < 0:
            img = pygame.transform.flip(img, True, False)

        # 🔑 visual offset (lower sprite, keep hitbox correct)
        SPRITE_Y_OFFSET = 0

        surface.blit(
            img,
            (self.rect.x - cam[0], self.rect.y - cam[1] + SPRITE_Y_OFFSET)
        )

