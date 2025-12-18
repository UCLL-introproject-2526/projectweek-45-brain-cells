from level.base_level import BaseLevel
from level.tile import Tile
from level.obstacle import PushBlock
from level.devices import Switch, Door, Finish, HoldPlate, LatchPlate
from level.spikes import Spike
from level.checkpoint import Checkpoint
from level.cannon import Cannon
from settings import TILE_SIZE
from level.ground import Ground
from level.left_wall import LWall
from level.right_wall import RWall
from level.left_corner import LCorner
from level.right_corner import RCorner
from level.left_drop import LDrop
from level.right_drop import RDrop
from level.downside import Down, RDown, LDown
from level.inner import LInner, RInner
from level.deco import Deco
from level.tekst import T1,T2,T3,T4
import pygame
from assets.goblins import load_goblin_sprites
from level.goblin import Goblin  
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
        self.bg_rect = img.get_rect()
        self.bg_rect.bottom = world_h  # 🔑 align to bottom tile

    
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

                elif ch == "F":
                    self.finish = Finish(wx, wy - TILE_SIZE)

                
                elif ch == "G":
                    self.goblins.append(Goblin(
                            x * TILE_SIZE,
                            y * TILE_SIZE,
                            self.goblin_sprites
                        )
                    )
                elif ch == "p":
                    self.plates.append(
                        HoldPlate(
                            x*TILE_SIZE,
                            y*TILE_SIZE + TILE_SIZE - 12,
                            key="A"
                        )
                    )

                elif ch == "P":
                    self.plates.append(
                        LatchPlate(
                            x*TILE_SIZE,
                            y*TILE_SIZE + TILE_SIZE - 12,
                            key="B"
                        )
                    )


                elif ch == "D":
                    self.doors.append(
                        Door(
                            x*TILE_SIZE,
                            y*TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE,
                            key="B",
                            mode="latch",
                            logic="AND"
                        )
                    )

                elif ch == "d":  # OR door
                    self.doors.append(
                        Door(
                            x*TILE_SIZE,
                            y*TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE,
                            key="A",
                            mode="hold",
                            logic="OR"
                        )
                    )



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
                
                elif ch == "l":
                    self.left_wall.append(LWall(wx, wy, TILE_SIZE))
                
                elif ch == "r":
                    self.right_wall.append(RWall(wx,wy, TILE_SIZE))

                elif ch == "L":
                    self.left_corner.append(LCorner(wx, wy, TILE_SIZE))
                
                elif ch == "R":
                    self.right_corner.append(RCorner(wx,wy, TILE_SIZE))
                
                elif ch == "(":
                    self.left_drop.append(LDrop(wx, wy, TILE_SIZE))
                
                elif ch == ")":
                    self.right_drop.append(RDrop(wx,wy, TILE_SIZE))
                
                elif ch == "]":
                    self.right_downside.append(RDown(wx,wy, TILE_SIZE))
                
                elif ch == "[":
                    self.left_downside.append(LDown(wx,wy, TILE_SIZE))
                
                elif ch == "u":
                    self.downside.append(Down(wx,wy, TILE_SIZE))

                elif ch == "é":
                    self.left_inner.append(LInner(wx,wy, TILE_SIZE))

                elif ch == "è":
                    self.right_inner.append(RInner(wx,wy, TILE_SIZE))

                elif ch == "/":
                    self.deco.append(Deco(wx,wy, TILE_SIZE))
                
                elif ch == "3":
                    self.deco.append(T1(wx,wy, TILE_SIZE*5))
                
                elif ch == "4":
                    self.deco.append(T2(wx,wy, TILE_SIZE*5))

                elif ch == "6":
                    self.deco.append(T4(wx,wy, TILE_SIZE*5))

                elif ch == "5":
                    self.deco.append(T3(wx,wy, TILE_SIZE*5))