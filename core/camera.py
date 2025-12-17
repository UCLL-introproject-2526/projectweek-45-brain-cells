import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self, world_height):
        self.pos = pygame.Vector2(0, 0)
        self.world_height = world_height

    def update(self, target_rects):
        if not target_rects:
            return

        minx = min(r.left for r in target_rects)
        maxx = max(r.right for r in target_rects)
        miny = min(r.top for r in target_rects)
        maxy = max(r.bottom for r in target_rects)

        center = pygame.Vector2(
            (minx + maxx) / 2,
            (miny + maxy) / 2
        )

        desired = center - pygame.Vector2(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2
        )

        # smooth follow
        self.pos += (desired - self.pos) * 0.12

        # ────────────── CLAMP ──────────────
        max_y = max(0, self.world_height - SCREEN_HEIGHT)

        self.pos.x = max(0, self.pos.x)
        self.pos.y = max(0, min(self.pos.y, max_y))

    def offset(self):
        return int(self.pos.x), int(self.pos.y)
