import pygame
from core.entity import Entity
from core.physics import PhysicsBody
from settings import MERGED_W, MERGED_H, MERGED_SPEED, MERGED_JUMP

JUMP_BUFFER_TIME = 0.12
COYOTE_TIME = 0.12


class MergedPlayer(Entity, PhysicsBody):
    def __init__(self, x, y, input_a, input_b):
        Entity.__init__(self, x, y, MERGED_W, MERGED_H)
        PhysicsBody.__init__(self)

        self.input_a = input_a
        self.input_b = input_b

        self.jump_buffer = 0.0
        self.coyote_timer = 0.0

    def wants_split(self):
        return self.input_a.merge_pressed() or self.input_b.merge_pressed()

    def update(self, dt, solids, blocks):
        # Gravity
        self.apply_gravity()

        # Horizontal input
        axis = self.input_a.axis() + self.input_b.axis()
        axis = max(-1, min(1, axis))
        self.vel.x = axis * MERGED_SPEED

        # Jump buffering
        if self.input_a.jump_pressed() or self.input_b.jump_pressed():
            self.jump_buffer = JUMP_BUFFER_TIME
        else:
            self.jump_buffer = max(0.0, self.jump_buffer - dt)

        # Coyote time
        if self.on_ground:
            self.coyote_timer = COYOTE_TIME
        else:
            self.coyote_timer = max(0.0, self.coyote_timer - dt)

        if self.jump_buffer > 0 and self.coyote_timer > 0:
            self.vel.y = MERGED_JUMP
            self.jump_buffer = 0
            self.coyote_timer = 0

        # 🔑 PUSH BLOCKS BEFORE COLLISION RESOLUTION
        self._push_blocks(blocks)

        # Resolve terrain + block collisions (vertical correctness)
        self.move_and_collide(self.rect, solids, dt)

    def _push_blocks(self, blocks):
        for b in blocks:
            if not self.rect.colliderect(b.rect):
                continue

            dx = self.vel.x
            if dx == 0:
                continue

            # Check that collision is horizontal
            overlap_x = min(self.rect.right, b.rect.right) - max(self.rect.left, b.rect.left)
            overlap_y = min(self.rect.bottom, b.rect.bottom) - max(self.rect.top, b.rect.top)

            if overlap_x < overlap_y:
                if dx > 0:
                    b.rect.x += dx
                    self.rect.right = b.rect.left
                elif dx < 0:
                    b.rect.x += dx
                    self.rect.left = b.rect.right

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, (190, 70, 210), r, border_radius=10)
        pygame.draw.rect(surface, (10, 10, 10), r, 3, border_radius=10)
