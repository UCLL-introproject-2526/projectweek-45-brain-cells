from level.base_level import BaseLevel
from level.tile import Tile
from level.obstacle import PushBlock
from level.devices import Switch, Door, Goal
from level.spikes import Spike
from level.checkpoint import Checkpoint
from level.cannon import Cannon
from settings import TILE_SIZE
from level.ground import Ground
from level.wall import Wall
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class AsciiLevel(BaseLevel):
    map_data = []

    def __init__(self):
        super().__init__()
        self.background = None
    
    def load_background(self, path):
        img = pygame.image.load(path).convert()
        world_w = len(self.map_data[0]) * TILE_SIZE
        world_h = len(self.map_data) * TILE_SIZE
        img = pygame.transform.scale(img, (world_w, world_h))
        self.background = img
    
    def draw_background(self, screen, cam, t):
        if self.background:
            cam_x, cam_y = cam
            factor = 0.3
            screen.blit(self.background, (-cam_x * factor, -cam_y * factor))
        else:
            screen.fill((0, 0, 0))

    def build(self):
        if not self.map_data:
            raise ValueError("AsciiLevel.map_data is empty")
        self.build_from_ascii(self.map_data)

    def build_from_ascii(self, data):
        for y, row in enumerate(data):
            for x, ch in enumerate(row):
                wx = x * TILE_SIZE
                wy = y * TILE_SIZE

                if ch == "#":
                    self.tiles.append(Tile(wx, wy, TILE_SIZE))

                elif ch == "B":
                    self.blocks.append(PushBlock(wx, wy - TILE_SIZE))

                elif ch == "S":
                    self.spikes.append(Spike(wx, wy))

                elif ch == "G":
                    self.goal = Goal(wx, wy)

                elif ch == "C":
                    self.checkpoints.append(Checkpoint(wx, wy))

                elif ch in "<>^v":
                    self.cannons.append(Cannon(wx, wy, ch))

                elif ch == "1":
                    self.spawn_p1 = (wx, wy)

                elif ch == "2":
                    self.spawn_p2 = (wx, wy)
                
                elif ch == "@":
                    self.ground.append(Ground(wx, wy, TILE_SIZE))
                
                elif ch == "i":
                    self.wall.append(Wall(wx, wy, TILE_SIZE))
