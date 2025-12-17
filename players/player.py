import pygame
from core.entity import Entity
from settings import (
    PLAYER_W, PLAYER_H,
    PLAYER_SPEED, PLAYER_JUMP,
    GRAVITY
)

LAND_EPSILON = 6
ANIM_FPS = 10  # walking animation speed


class Player(Entity):
    def __init__(self, x, y, input_handler, variant="white"):
        super().__init__(x, y, PLAYER_W, PLAYER_H)

        self.input = input_handler
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.variant = variant

        # previous frame rect (for temporal checks)
        self.prev_rect = self.rect.copy()

        # prevents compression explosion
        self.standing_on_player = False

        # -------------------------
        # SPRITES / ANIMATION
        # -------------------------
        self.variant = variant.lower()
        self.walk_frames = self._load_walk_frames()
        self.frame_index = 0
        self.anim_timer = 0.0
        self.facing_right = True

        # scale sprites to hitbox
        self.walk_frames = [
            pygame.transform.smoothscale(img, (PLAYER_W, PLAYER_H))
            for img in self.walk_frames
        ]

    # --------------------------------------------------
    # LOAD SPRITES
    # --------------------------------------------------
    def _load_walk_frames(self):
        frames = []
        for i in range(4):
            img = pygame.image.load(
                f"assets/hero/{self.variant}_{i+1}.png"
            ).convert_alpha()
            frames.append(img)
        return frames

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------
    def update(self, dt, solids, other_players):
        # store previous state
        self.prev_rect = self.rect.copy()
        self.standing_on_player = False

        # -------------------------
        # INPUT
        # -------------------------
        axis = self.input.axis()
        self.vel.x = axis * PLAYER_SPEED

        if axis != 0:
            self.facing_right = axis > 0

        if self.on_ground and self.input.jump_pressed():
            self.vel.y = PLAYER_JUMP

        # gravity
        self.vel.y += GRAVITY

        # ==================================================
        # HORIZONTAL MOVE
        # ==================================================
        self.rect.x += int(self.vel.x)

        # tiles
        for s in solids:
            if self.rect.bottom > s.rect.top and self.rect.top < s.rect.bottom:
                if self.rect.colliderect(s.rect):
                    if self.vel.x > 0:
                        self.rect.right = s.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = s.rect.right

        # players (horizontal block ONLY)
        for p in other_players:
            if not self.rect.colliderect(p.rect):
                continue

            if self.rect.bottom > p.rect.top and self.rect.top < p.rect.bottom:
                if self.vel.x > 0:
                    self.rect.right = p.rect.left
                elif self.vel.x < 0:
                    self.rect.left = p.rect.right

        # ==================================================
        # VERTICAL MOVE
        # ==================================================
        self.on_ground = False
        self.rect.y += int(self.vel.y)

        # -------- tiles --------
        for s in solids:
            if not self.rect.colliderect(s.rect):
                continue

            # floor
            if self.vel.y > 0:
                self.rect.bottom = s.rect.top
                self.vel.y = 0
                self.on_ground = True

            # ceiling
            elif self.vel.y < 0 and not self.standing_on_player:
                self.rect.top = s.rect.bottom
                self.vel.y = 0

        # -------- players --------
        for p in other_players:
            if not self.rect.colliderect(p.rect):
                continue

            # landing on player
            if (
                self.vel.y > 0 and
                self.prev_rect.bottom <= p.rect.top + LAND_EPSILON
            ):
                self.rect.bottom = p.rect.top
                self.vel.y = 0
                self.on_ground = True
                self.standing_on_player = True

            # hit from below
            elif (
                self.vel.y < 0 and
                self.prev_rect.top >= p.rect.bottom - LAND_EPSILON
            ):
                self.rect.top = p.rect.bottom
                self.vel.y = 0

        # ==================================================
        # ANIMATION UPDATE
        # ==================================================
        # ==================================================
# ANIMATION UPDATE (FIXED)
# ==================================================
        moving = abs(self.vel.x) > 0.1

        if moving:
            self.anim_timer += dt
            if self.anim_timer >= 1 / ANIM_FPS:
                self.anim_timer -= 1 / ANIM_FPS
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
        else:
            self.anim_timer = 0
            self.frame_index = 0


    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------
    def draw(self, surface, cam):
        img = self.walk_frames[self.frame_index]

        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        r = self.rect.move(-cam[0], -cam[1])
        surface.blit(img, r.topleft)
