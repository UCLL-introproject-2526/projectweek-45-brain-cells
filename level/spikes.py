import pygame
from core.entity import Entity
from settings import TILE_SIZE


class Spike(Entity):
    def __init__(self, x, y, w=TILE_SIZE, h=TILE_SIZE):
        super().__init__(x, y, w, h)

        # precompute triangle points in WORLD space
        self.a = pygame.Vector2(self.rect.left, self.rect.bottom)
        self.b = pygame.Vector2(self.rect.centerx, self.rect.top)
        self.c = pygame.Vector2(self.rect.right, self.rect.bottom)

    # -------------------------
    # TRIANGLE COLLISION
    # -------------------------
    def collides(self, actor_rect):
        """
        Returns True if actor touches the spike triangle.
        """
        # Broad phase (cheap)
        if not self.rect.colliderect(actor_rect):
            return False

        # Test key points of the actor (feet + center)
        test_points = [
            actor_rect.midbottom,
            actor_rect.bottomleft,
            actor_rect.bottomright,
            actor_rect.center
        ]

        for p in test_points:
            if self._point_in_triangle(p):
                return True

        return False

    def _point_in_triangle(self, p):
        p = pygame.Vector2(p)

        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - \
                   (p2.x - p3.x) * (p1.y - p3.y)

        d1 = sign(p, self.a, self.b)
        d2 = sign(p, self.b, self.c)
        d3 = sign(p, self.c, self.a)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)
    
    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])

        points = [
            (r.left, r.bottom),
            (r.centerx, r.top),
            (r.right, r.bottom)
        ]

        pygame.draw.polygon(surface, (180, 180, 190), points)

