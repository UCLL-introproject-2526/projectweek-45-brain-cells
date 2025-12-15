from level.base_level import BaseLevel, Torch
from level.tile import Tile
from level.obstacle import PushBlock
from level.devices import Goal
from level.spikes import Spike
from level.checkpoint import Checkpoint
from settings import TILE_SIZE

class AsciiLevel(BaseLevel):
    """
    Define a level by setting:
      - name: str
      - map_data: list[str]  (ASCII rows, top->bottom)

    Legend (you can extend this easily):
      # = solid tile
      ^ = spikes
      G = goal
      C = checkpoint
      1 = player1 spawn
      2 = player2 spawn
      B = push block
      T = torch (background glow)
      . / space = empty
    """

    name = "Unnamed"
    map_data = []

    def build(self):
        self.build_from_ascii(self.map_data)

    def build_from_ascii(self, rows):
        if not rows:
            raise ValueError("AsciiLevel.map_data is empty")

        h = len(rows)
        w = max(len(r) for r in rows)

        # defaults if not set by map
        self.spawn_p1 = (120, 100)
        self.spawn_p2 = (200, 100)

        for y, row in enumerate(rows):
            for x, ch in enumerate(row.ljust(w)):
                wx = x * TILE_SIZE
                wy = y * TILE_SIZE

                if ch == "#":
                    self.tiles.append(Tile(wx, wy, TILE_SIZE, variant=(x + y) % 2))

                elif ch == "^":
                    # smaller spikes by default (fairer)
                    self.spikes.append(Spike(wx + 8, wy + TILE_SIZE - 16, w=32, h=16))

                elif ch == "G":
                    self.goal = Goal(wx, wy - (TILE_SIZE * 1))  # slightly up for look

                elif ch == "C":
                    self.checkpoints.append(Checkpoint(wx + 8, wy + (TILE_SIZE - 48)))

                elif ch == "1":
                    self.spawn_p1 = (wx, wy)

                elif ch == "2":
                    self.spawn_p2 = (wx, wy)

                elif ch == "B":
                    self.blocks.append(PushBlock(wx, wy))

                elif ch == "T":
                    # torch is a background thing; place a little above tile center
                    self.torches.append(Torch(wx + TILE_SIZE // 2, wy + TILE_SIZE // 2))

        # If no goal found, that’s okay (but you probably want one)
