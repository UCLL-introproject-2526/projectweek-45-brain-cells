import pygame
from core.entity import Entity
from core.physics import PhysicsBody
from settings import MERGED_W, MERGED_H, MERGED_SPEED, MERGED_JUMP

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

    def wants_split(self):
        # either can trigger split
        return self.input_a.merge_pressed() or self.input_b.merge_pressed()

    def update(self, dt, solids, blocks):
        self.apply_gravity()

        axis = self.input_a.axis() + self.input_b.axis()
        axis = max(-1, min(1, axis))
        self.vel.x = axis * MERGED_SPEED

        if (self.input_a.jump_pressed() or self.input_b.jump_pressed()) and self.on_ground:
            self.vel.y = MERGED_JUMP

        # If pushing blocks, allow motion transfer
        self._push_blocks(blocks)

        self.move_and_collide(self.rect, solids, dt)

    def _push_blocks(self, blocks):
        # If we're overlapping on the side, impart velocity to block
        for b in blocks:
            if not self.rect.colliderect(b.rect):
                continue

            # only push if collision is mostly horizontal
            overlap_x = min(self.rect.right, b.rect.right) - max(self.rect.left, b.rect.left)
            overlap_y = min(self.rect.bottom, b.rect.bottom) - max(self.rect.top, b.rect.top)
            if overlap_x <= 0 or overlap_y <= 0:
                continue
            if overlap_x < overlap_y:
                # push direction based on where we are
                if self.rect.centerx < b.rect.centerx:
                    b.vel.x = max(b.vel.x, self.vel.x)
                else:
                    b.vel.x = min(b.vel.x, self.vel.x)

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, (190, 70, 210), r, border_radius=10)
        pygame.draw.rect(surface, (10, 10, 10), r, 3, border_radius=10)
