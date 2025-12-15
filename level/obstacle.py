import pygame
from core.entity import Entity
from core.physics import PhysicsBody
from settings import BLOCK_FRICTION, BLOCK_MAX_SPEED

class PushBlock(Entity, PhysicsBody):
    """
    Heavy block: only MergedPlayer can push it.
    We simulate simple horizontal pushing with friction.
    """
    def __init__(self, x, y, w=48, h=48):
        Entity.__init__(self, x, y, w, h)
        PhysicsBody.__init__(self)
        self.is_heavy = True

    def update(self, dt, solids):
        # gravity + collide like a body
        self.apply_gravity()
        self.move_and_collide(self.rect, solids, dt)

        # friction
        self.vel.x *= BLOCK_FRICTION
        if abs(self.vel.x) < 0.05:
            self.vel.x = 0
        self.vel.x = max(-BLOCK_MAX_SPEED, min(BLOCK_MAX_SPEED, self.vel.x))

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, (110, 90, 60), r)
        pygame.draw.rect(surface, (25, 20, 15), r, 3)
