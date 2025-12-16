import pygame
from core.entity import Entity
from settings import (
    PLAYER_W, PLAYER_H,
    PLAYER_SPEED, PLAYER_JUMP,
    GRAVITY
)


class Player(Entity):
    def __init__(self, x, y, input_handler, color):
        super().__init__(x, y, PLAYER_W, PLAYER_H)
        self.input = input_handler
        self.color = color
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False

    def update(self, dt, solids, other_players):
        # -------------------------
        # INPUT
        # -------------------------
        axis = self.input.axis()
        self.vel.x = axis * PLAYER_SPEED

        if self.on_ground and self.input.jump_pressed():
            self.vel.y = PLAYER_JUMP

        # gravity
        self.vel.y += GRAVITY

        # -------------------------
        # HORIZONTAL MOVE
        # (tiles / blocks ONLY)
        # -------------------------
        self.rect.x += int(self.vel.x)

        for s in solids:
            # only block sideways movement if overlapping vertically
            if self.rect.bottom > s.rect.top and self.rect.top < s.rect.bottom:
                if self.rect.colliderect(s.rect):
                    if self.vel.x > 0:
                        self.rect.right = s.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = s.rect.right

        # -------------------------
        # VERTICAL MOVE
        # (tiles + players)
        # -------------------------
        self.on_ground = False
        self.rect.y += int(self.vel.y)

        for s in solids + other_players:
            if self.rect.colliderect(s.rect):
                if self.vel.y > 0:
                    self.rect.bottom = s.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = s.rect.bottom
                    self.vel.y = 0

    def draw(self, surface, cam):
        r = self.rect.move(-cam[0], -cam[1])
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (20, 20, 20), r, 2)
