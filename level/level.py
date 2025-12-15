import random
import math
import pygame
from settings import TILE_SIZE
from level.tile import Tile
from level.obstacle import PushBlock
from level.devices import Switch, Door, Goal
from level.spikes import Spike


class Torch:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.phase = random.random() * 10

    def draw(self, surface, camera_offset, t):
        ox, oy = camera_offset
        x, y = int(self.pos.x - ox), int(self.pos.y - oy)

        pygame.draw.rect(surface, (60, 45, 30), pygame.Rect(x - 3, y, 6, 16))

        flick = 0.6 + 0.4 * (0.5 + 0.5 * math.sin((t + self.phase) * 6.0))
        radius = int(50 * flick)

        glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 170, 60, 70), (radius, radius), radius)
        pygame.draw.circle(glow, (255, 200, 80, 85), (radius, radius), int(radius * 0.55))
        surface.blit(glow, (x - radius, y - radius))

        pygame.draw.circle(surface, (255, 170, 60), (x, y - 2), 4)
        pygame.draw.circle(surface, (255, 220, 120), (x, y - 3), 2)


class Level:
    def __init__(self):
        self.tiles = []
        self.blocks = []
        self.switches = []
        self.doors = []
        self.spikes = []
        self.torches = []
        self.goal = None
        self._build()

    def solids(self):
        solids = list(self.tiles)
        solids += [d for d in self.doors if d.solid]
        solids += self.blocks
        return solids

    def actors_for_switches(self, actors):
        return list(actors) + list(self.blocks)

    def _build_platform(self, x0, x1, y, variant=0):
        for x in range(x0, x1):
            self.tiles.append(Tile(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, variant))

    def _build(self):
        self._build_platform(0, 60, 10, variant=1)
        self._build_platform(6, 12, 8)
        self._build_platform(14, 18, 7)
        self._build_platform(20, 25, 8)
        self._build_platform(27, 30, 8)
        self._build_platform(33, 37, 6)
        self._build_platform(39, 43, 6)

        s1 = Switch(45 * TILE_SIZE, 10 * TILE_SIZE - 12)
        s2 = Switch(48 * TILE_SIZE, 10 * TILE_SIZE - 12)
        self.switches += [s1, s2]

        self.doors.append(Door(
            51 * TILE_SIZE, 10 * TILE_SIZE - 96,
            w=TILE_SIZE, h=96, requires=[s1, s2]
        ))

        self._build_platform(52, 56, 9)
        self._build_platform(58, 62, 8)

        self.blocks.append(PushBlock(56 * TILE_SIZE, 9 * TILE_SIZE - 48))

        s3 = Switch(62 * TILE_SIZE, 10 * TILE_SIZE - 12)
        self.switches.append(s3)

        self.doors.append(Door(
            65 * TILE_SIZE, 10 * TILE_SIZE - 96,
            w=TILE_SIZE, h=96, requires=[s3]
        ))

        self._build_platform(66, 70, 9)
        self._build_platform(71, 74, 7)
        self._build_platform(75, 78, 5)

        self.goal = Goal(79 * TILE_SIZE, 10 * TILE_SIZE - 96)

        for tx in [4, 10, 18, 26, 34, 42, 50, 58, 66, 74, 80]:
            self.torches.append(Torch(tx * TILE_SIZE + TILE_SIZE // 2, 9 * TILE_SIZE - 60))

        # Spikes (punishment zones)
        for sx in [35, 36, 37]:
            self.spikes.append(Spike(sx * TILE_SIZE, 10 * TILE_SIZE - 24))

    def update(self, dt, actors):
        base_solids = list(self.tiles) + [d for d in self.doors if d.solid]
        for b in self.blocks:
            b.update(dt, base_solids)

        for s in self.switches:
            s.update(dt, self.actors_for_switches(actors))

        for d in self.doors:
            d.update(dt)

    def draw_background(self, surface, camera_offset, t):
        surface.fill((12, 12, 18))
        ox, oy = camera_offset

        for by in range(14):
            for bx in range(30):
                x = bx * TILE_SIZE - (ox % TILE_SIZE)
                y = by * TILE_SIZE - (oy % TILE_SIZE)
                r = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                col = (20, 20, 28) if (bx + by) % 2 == 0 else (24, 24, 33)
                pygame.draw.rect(surface, col, r)
                pygame.draw.rect(surface, (10, 10, 14), r, 1)

        for torch in self.torches:
            torch.draw(surface, camera_offset, t)

    def draw(self, surface, camera_offset):
        for tile in self.tiles:
            tile.draw(surface, camera_offset)
        for s in self.switches:
            s.draw(surface, camera_offset)
        for d in self.doors:
            d.draw(surface, camera_offset)
        for b in self.blocks:
            b.draw(surface, camera_offset)
        for sp in self.spikes:
            sp.draw(surface, camera_offset)
        if self.goal:
            self.goal.draw(surface, camera_offset)
