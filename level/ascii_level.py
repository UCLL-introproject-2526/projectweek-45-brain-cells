from level.base_level import BaseLevel
from level.tile import Tile
from level.obstacle import PushBlock
from level.devices import Switch, Door, Goal
from level.spikes import Spike
from level.checkpoint import Checkpoint
from level.cannon import Cannon
from settings import TILE_SIZE
from level.ground import Ground

class AsciiLevel(BaseLevel):
    map_data = []

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
                    self.spikes.append(Spike(wx, wy + TILE_SIZE - 24))

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
