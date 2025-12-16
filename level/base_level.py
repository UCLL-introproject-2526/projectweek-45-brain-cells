import pygame
import random
import math
from settings import TILE_SIZE


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


class BaseLevel:
    def __init__(self):
        self.tiles = []
        self.blocks = []
        self.switches = []
        self.doors = []
        self.spikes = []
        self.torches = []
        self.checkpoints = []
        self.cannons = []
        self.cannonballs = []
        self.goal = None

        self.spawn_p1 = (120, 100)
        self.spawn_p2 = (200, 100)

        self.respawn_p1 = self.spawn_p1
        self.respawn_p2 = self.spawn_p2

        self.build()

        self.respawn_p1 = self.spawn_p1
        self.respawn_p2 = self.spawn_p2

    def build(self):
        raise NotImplementedError

    # -------------------------
    # SOLIDS
    # -------------------------
    def solids(self):
        solids = list(self.tiles)
        solids += [d for d in self.doors if d.solid]
        solids += self.blocks
        solids += self.cannons   # 🔑 cannons are solid
        return solids

    def actors_for_switches(self, actors):
        return list(actors) + list(self.blocks)

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, dt, actors):
        base_solids = list(self.tiles) + [d for d in self.doors if d.solid] + self.cannons

        # Blocks
        for b in self.blocks:
            solids_without_self = base_solids + [o for o in self.blocks if o is not b]
            b.update(solids_without_self)


        # Switches
        for s in self.switches:
            s.update(dt, self.actors_for_switches(actors))

        # Doors
        for d in self.doors:
            d.update(dt)

        # Cannons
        for c in self.cannons:
            c.update(dt, self)

        # Cannonballs
        for ball in self.cannonballs[:]:
            ball.update(dt)

            # 🔑 REMOVE ON SOLID HIT
            for solid in base_solids + self.blocks:
                if solid is ball.owner:
                    continue
                if ball.rect.colliderect(solid.rect):
                    self.cannonballs.remove(ball)
                    break


        # Checkpoints (merged only)
        merged = actors[0] if len(actors) == 1 else None
        for cp in self.checkpoints:
            cp.try_activate(merged, self)

    # -------------------------
    # DRAW
    # -------------------------
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
        for cp in self.checkpoints:
            cp.draw(surface, camera_offset)
        for c in self.cannons:
            c.draw(surface, camera_offset)
        for ball in self.cannonballs:
            ball.draw(surface, camera_offset)
        if self.goal:
            self.goal.draw(surface, camera_offset)
