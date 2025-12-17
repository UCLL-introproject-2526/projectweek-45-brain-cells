import pygame
from settings import TILE_SIZE


class Grid:
    def __init__(self, grid_w, grid_h):
        self.grid_w = grid_w
        self.grid_h = grid_h

    def world_to_cell(self, wx, wy):
        return int(wx // TILE_SIZE), int(wy // TILE_SIZE)

    def cell_to_world(self, cx, cy):
        return cx * TILE_SIZE, cy * TILE_SIZE

    def draw_lines(self, surface, camera):
        color = (40, 40, 60)

        for x in range(self.grid_w + 1):
            sx = x * TILE_SIZE - camera.pos.x
            pygame.draw.line(surface, color, (sx, 0), (sx, surface.get_height()))

        for y in range(self.grid_h + 1):
            sy = y * TILE_SIZE - camera.pos.y
            pygame.draw.line(surface, color, (0, sy), (surface.get_width(), sy))

    def draw_highlight(self, surface, camera, cx, cy):
        if not (0 <= cx < self.grid_w and 0 <= cy < self.grid_h):
            return

        wx, wy = self.cell_to_world(cx, cy)
        rect = pygame.Rect(
            wx - camera.pos.x,
            wy - camera.pos.y,
            TILE_SIZE,
            TILE_SIZE
        )
        pygame.draw.rect(surface, (200, 200, 240), rect, 2)
