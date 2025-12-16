import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, rects):
        # existing behavior (keep)
        if not rects:
            return

        avg_x = sum(r.centerx for r in rects) / len(rects)
        avg_y = sum(r.centery for r in rects) / len(rects)

        self.x = avg_x - SCREEN_WIDTH // 2
        self.y = avg_y - SCREEN_HEIGHT // 2

    def follow_single(self, rect, view_w, view_h):
        """
        Hard lock camera to a single rect (used for split screen)
        """
        self.x = rect.centerx - view_w // 2
        self.y = rect.centery - view_h // 2

    def offset(self):
        return int(self.x), int(self.y)

