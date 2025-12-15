import pygame
from core.entity import Entity
from core.physics import PhysicsBody
from settings import BLOCK_FRICTION


class PushBlock(Entity, PhysicsBody):
    def __init__(self, x, y, w=48, h=48):
        Entity.__init__(self, x, y, w, h)
        PhysicsBody.__init__(self)

        # 🔑 Stable initial state
        self.vel.xy = (0, 0)
        self.on_ground = False

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)

    def update(self, dt, solids):
        self.apply_gravity()

        self.vel.x *= BLOCK_FRICTION
        if abs(self.vel.x) < 0.05:
            self.vel.x = 0

        # solids NEVER include self (guaranteed by BaseLevel)
        self.move_and_collide(self.rect, solids, dt)

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, (120, 90, 60), r)
        pygame.draw.rect(surface, (30, 30, 30), r, 3)
