import pygame
from core.entity import Entity
from settings import (
    TILE_SIZE, GRAVITY,
    MERGED_W, MERGED_H,
    MERGED_SPEED, MERGED_JUMP,
    GRAB_KEY, GRAB_RANGE
)


class MergedPlayer(Entity):
    def __init__(self, x, y, input1, input2):
        super().__init__(x, y, MERGED_W, MERGED_H)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.input1 = input1
        self.input2 = input2
        self.grabbed_block = None

        # 🔑 prevents sideways impulse on merge frame
        self.just_merged = True

    def wants_split(self):
        return self.input1.merge_pressed() or self.input2.merge_pressed()

    def _find_block(self, blocks):
        for b in blocks:
            vertical = self.rect.bottom > b.rect.top and self.rect.top < b.rect.bottom
            horizontal = abs(self.rect.centerx - b.rect.centerx) <= TILE_SIZE + GRAB_RANGE
            if vertical and horizontal:
                return b
        return None

    def update(self, dt, solids, blocks):
        # 🔑 lock movement on merge frame
        if self.just_merged:
            self.vel.x = 0
            self.just_merged = False

        axis = self.input1.axis() + self.input2.axis()
        axis = max(-1, min(1, axis))
        self.vel.x = axis * MERGED_SPEED

        if not self.grabbed_block and pygame.key.get_pressed()[GRAB_KEY]:
            block = self._find_block(blocks)
            if block:
                self.grabbed_block = block
                block.grabbed = True
        elif self.grabbed_block and not pygame.key.get_pressed()[GRAB_KEY]:
            self.grabbed_block.grabbed = False
            self.grabbed_block = None

        if not self.grabbed_block and self.on_ground:
            if self.input1.jump_pressed() or self.input2.jump_pressed():
                self.vel.y = MERGED_JUMP

        self.vel.y += GRAVITY

        # horizontal (tiles only)
        self.rect.x += int(self.vel.x)
        for s in solids:
            if self.rect.bottom > s.rect.top and self.rect.top < s.rect.bottom:
                if self.rect.colliderect(s.rect):
                    if self.vel.x > 0:
                        self.rect.right = s.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = s.rect.right

        if self.grabbed_block:
            self.grabbed_block.vel.x = self.vel.x

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

    def draw(self, surface, cam):
        r = self.rect.move(-cam[0], -cam[1])
        pygame.draw.rect(surface, (160, 80, 200), r)
        pygame.draw.rect(surface, (60, 20, 80), r, 2)
