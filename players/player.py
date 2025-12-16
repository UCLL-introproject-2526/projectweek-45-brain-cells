import pygame
from core.entity import Entity
from settings import (
    PLAYER_W, PLAYER_H,
    PLAYER_SPEED, PLAYER_JUMP,
    GRAVITY
)

LAND_EPSILON = 6  # tolerance for landing checks


class Player(Entity):
    def __init__(self, x, y, input_handler, color):
        super().__init__(x, y, PLAYER_W, PLAYER_H)
        self.input = input_handler
        self.color = color
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False

        # 🔑 store previous position
        self.prev_rect = self.rect.copy()

    def update(self, dt, solids, other_players):
        # store previous rect
        self.prev_rect = self.rect.copy()

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
        # HORIZONTAL MOVE (tiles only)
        # -------------------------
        self.rect.x += int(self.vel.x)

        for s in solids:
            if self.rect.bottom > s.rect.top and self.rect.top < s.rect.bottom:
                if self.rect.colliderect(s.rect):
                    if self.vel.x > 0:
                        self.rect.right = s.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = s.rect.right

        # -------------------------
        # VERTICAL MOVE
        # -------------------------
        self.on_ground = False
        self.rect.y += int(self.vel.y)

        # tiles first
        for s in solids:
            if self.rect.colliderect(s.rect):
                if self.vel.y > 0:
                    self.rect.bottom = s.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = s.rect.bottom
                    self.vel.y = 0

        # players second (LANDING ONLY)
        for p in other_players:
            if not self.rect.colliderect(p.rect):
                continue

            # ✅ only land if we were above last frame
            if (
                self.vel.y > 0 and
                self.prev_rect.bottom <= p.rect.top + LAND_EPSILON
            ):
                self.rect.bottom = p.rect.top
                self.vel.y = 0
                self.on_ground = True

    def draw(self, surface, cam):
        r = self.rect.move(-cam[0], -cam[1])
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (20, 20, 20), r, 2)
