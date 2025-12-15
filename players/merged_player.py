import pygame
from core.entity import Entity
from core.physics import PhysicsBody
from settings import MERGED_W, MERGED_H, MERGED_SPEED, MERGED_JUMP

JUMP_BUFFER_TIME = 0.12
COYOTE_TIME = 0.12


class MergedPlayer(Entity, PhysicsBody):
    """
    One body controlled by BOTH players' inputs simultaneously.
    - heavier: can push heavy blocks
    - higher jump
    - slower movement
    """
    def __init__(self, x, y, input_a, input_b):
        Entity.__init__(self, x, y, MERGED_W, MERGED_H)
        PhysicsBody.__init__(self)

        self.input_a = input_a
        self.input_b = input_b

        # jump feel fixes
        self.jump_buffer = 0.0
        self.coyote_timer = 0.0

    def wants_split(self):
        # either can trigger split
        return self.input_a.merge_pressed() or self.input_b.merge_pressed()

    def update(self, dt, solids, blocks):
        self.apply_gravity()

        # Horizontal movement
        axis = self.input_a.axis() + self.input_b.axis()
        axis = max(-1, min(1, axis))
        self.vel.x = axis * MERGED_SPEED

        # Jump buffering (either can press jump)
        if self.input_a.jump_pressed() or self.input_b.jump_pressed():
            self.jump_buffer = JUMP_BUFFER_TIME
        else:
            self.jump_buffer = max(0.0, self.jump_buffer - dt)

        # Coyote time (based on grounded state from last collision)
        if self.on_ground:
            self.coyote_timer = COYOTE_TIME
        else:
            self.coyote_timer = max(0.0, self.coyote_timer - dt)

        # Execute jump if buffered + coyote available
        if self.jump_buffer > 0.0 and self.coyote_timer > 0.0:
            self.vel.y = MERGED_JUMP
            self.jump_buffer = 0.0
            self.coyote_timer = 0.0

        # Allow pushing blocks (only merged does this)
        self._push_blocks(blocks)

        # Move/collide
        self.move_and_collide(self.rect, solids, dt)

    def _push_blocks(self, blocks):
        for b in blocks:
            if not self.rect.colliderect(b.rect):
                continue

            overlap_x = min(self.rect.right, b.rect.right) - max(self.rect.left, b.rect.left)
            overlap_y = min(self.rect.bottom, b.rect.bottom) - max(self.rect.top, b.rect.top)
            if overlap_x <= 0 or overlap_y <= 0:
                continue

            # push only when collision is mostly horizontal
            if overlap_x < overlap_y:
                if self.rect.centerx < b.rect.centerx:
                    b.vel.x = max(b.vel.x, self.vel.x)
                else:
                    b.vel.x = min(b.vel.x, self.vel.x)

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, (190, 70, 210), r, border_radius=10)
        pygame.draw.rect(surface, (10, 10, 10), r, 3, border_radius=10)
