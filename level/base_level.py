import pygame
import random
import math
from assets.goblins import load_goblin_sprites
from settings import TILE_SIZE


# --------------------------------------------------
# TORCH (BACKGROUND DECORATION)
# --------------------------------------------------
class Torch:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.phase = random.random() * 10

    def draw(self, surface, camera_offset, t):
        ox, oy = camera_offset
        x, y = int(self.pos.x - ox), int(self.pos.y - oy)

        # torch handle
        pygame.draw.rect(surface, (60, 45, 30), pygame.Rect(x - 3, y, 6, 16))

        # flicker glow
        flick = 0.6 + 0.4 * (0.5 + 0.5 * math.sin((t + self.phase) * 6.0))
        radius = int(50 * flick)

        glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 170, 60, 70), (radius, radius), radius)
        pygame.draw.circle(glow, (255, 200, 80, 85), (radius, radius), int(radius * 0.55))
        surface.blit(glow, (x - radius, y - radius))

        # flame
        pygame.draw.circle(surface, (255, 170, 60), (x, y - 2), 4)
        pygame.draw.circle(surface, (255, 220, 120), (x, y - 3), 2)


# --------------------------------------------------
# BASE LEVEL
# --------------------------------------------------
class BaseLevel:
    def __init__(self):
        # geometry
        self.tiles = []
        self.blocks = []

        # 🔑 pressure system
        self.plates = []      # hold + latch plates
        self.doors = []

        # hazards / interactables
        self.spikes = []
        self.torches = []
        self.checkpoints = []
        self.cannons = []
        self.cannonballs = []

        # static geometry layers
        self.ground = []
        self.left_wall = []
        self.right_wall = []
        self.right_corner = []
        self.left_corner = []
        self.left_drop = []
        self.right_drop = []
        self.left_downside = []
        self.right_downside = []
        self.downside = []
        self.left_inner = []
        self.right_inner = []

        # Deco
        self.deco = []
        self.t1 = []
        self.t2 = []
        self.t3 = []
        self.t4 = []
        
        # enemies
        self.goblins = []
        self.goblin_sprites = load_goblin_sprites()

        # finish (renamed from goal)
        self.finish = None

        # spawn points
        self.spawn_p1 = (120, 100)
        self.spawn_p2 = (200, 100)
        self.respawn_p1 = self.spawn_p1
        self.respawn_p2 = self.spawn_p2

        self.build()

        # checkpoints may override respawn
        self.respawn_p1 = self.spawn_p1
        self.respawn_p2 = self.spawn_p2
    
        

    def build(self):
        raise NotImplementedError


    # --------------------------------------------------
    # SOLIDS
    # --------------------------------------------------
    def solids(self):
        """
        Anything returned here is treated as a blocking solid.
        Open doors are automatically excluded.
        """
        solids = list(self.tiles)
        solids += [d for d in self.doors if d.solid]
        solids += self.blocks
        solids += self.cannons     # cannons are solid
        solids += self.ground
        solids += self.left_wall
        solids += self.right_wall
        solids += self.left_corner
        solids += self.right_corner
        solids += self.left_corner
        solids += self.right_corner
        solids += self.left_drop
        solids += self.right_drop
        solids += self.left_downside
        solids += self.right_downside
        solids += self.downside
        solids += self.left_inner
        solids += self.right_inner
        return solids


    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------
    def update(self, dt, actors):
        # actors = [player1, player2] OR [merged]
        pressure_actors = list(actors) + self.blocks

        base_solids = (
            list(self.tiles)
            + [d for d in self.doors if d.solid]
            + self.cannons
        )

        # -----------------
        # BLOCKS
        # -----------------
        all_solids = self.solids()

        for b in self.blocks:
            solids_without_self = [s for s in all_solids if s is not b]
            b.update(solids_without_self)


        # -----------------
        # PRESSURE PLATES
        # -----------------
        for p in self.plates:
            p.update(pressure_actors)

        # -----------------
        # DOORS (MUST RUN AFTER PLATES)
        # -----------------
        for d in self.doors:
            d.update(self.plates, actors)
        

        # -----------------
        # GOBLINS
        # -----------------
        for g in self.goblins:
            g.update(dt, self.solids())

        # -----------------
        # CANNONS
        # -----------------
        for c in self.cannons:
            c.update(dt, self)

        # -----------------
        # CANNONBALLS
        # -----------------
        all_solids = self.solids()

        for ball in self.cannonballs[:]:
            ball.update(dt)

            for solid in all_solids:
                if solid is ball.owner:
                    continue
                if ball.rect.colliderect(solid.rect):
                    self.cannonballs.remove(ball)
                    break


        # -----------------
        # CHECKPOINTS (MERGED ONLY)
        # -----------------
        merged = actors[0] if len(actors) == 1 else None
        for cp in self.checkpoints:
            cp.try_activate(merged, self)


    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------
    def draw_background(self, surface, camera_offset, t):
        surface.fill((12, 12, 18))
        ox, oy = camera_offset

        # dungeon wall pattern
        for by in range(14):
            for bx in range(30):
                x = bx * TILE_SIZE - (ox % TILE_SIZE)
                y = by * TILE_SIZE - (oy % TILE_SIZE)
                r = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                col = (20, 20, 28) if (bx + by) % 2 == 0 else (24, 24, 33)
                pygame.draw.rect(surface, col, r)
                pygame.draw.rect(surface, (10, 10, 14), r, 1)

        # torches glow on top of wall
        for torch in self.torches:
            torch.draw(surface, camera_offset, t)

    def draw(self, surface, camera_offset):
        # tiles first (true background)
        for tile in self.tiles:
            tile.draw(surface, camera_offset)

        # plates sit on ground
        for p in self.plates:
            p.draw(surface, camera_offset)

        # doors draw ONLY if closed
        for d in self.doors:
            d.draw(surface, camera_offset)

        # foreground solids & actors
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

        for ground in self.ground:
            ground.draw(surface, camera_offset)

        for left_wall in self.left_wall:
            left_wall.draw(surface, camera_offset)

        for right_wall in self.right_wall:
            right_wall.draw(surface, camera_offset)
        
        for left_corner in self.left_corner:
            left_corner.draw(surface, camera_offset)

        for right_corner in self.right_corner:
            right_corner.draw(surface, camera_offset)

        for left_drop in self.left_drop:
            left_drop.draw(surface, camera_offset)

        for right_drop in self.right_drop:
            right_drop.draw(surface, camera_offset)

        for left_downside in self.left_downside:
            left_downside.draw(surface, camera_offset)
        
        for right_downside in self.right_downside:
            right_downside.draw(surface, camera_offset)

        for downside in self.downside:
            downside.draw(surface, camera_offset)

        for g in self.goblins:
            g.draw(surface, camera_offset)
        
        for left_inner in self.left_inner:
            left_inner.draw(surface, camera_offset)
        
        for right_inner in self.right_inner:
            right_inner.draw(surface, camera_offset)
        
        for deco in self.deco:
            deco.draw(surface, camera_offset)
        
        for t1 in self.t1:
            t1.draw(surface, camera_offset)
        
        for t3 in self.t3:
            t3.draw(surface, camera_offset)
        
        for t2 in self.t2:
            t2.draw(surface, camera_offset)

        for t4 in self.t4:
            t4.draw(surface, camera_offset)

        if self.finish:
            self.finish.draw(surface, camera_offset)
