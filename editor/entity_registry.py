# editor/entity_registry.py

from level.tile import Tile
from level.obstacle import PushBlock
from level.spikes import Spike
from level.cannon import Cannon
from level.devices import Door, Finish, HoldPlate, LatchPlate
from level.checkpoint import Checkpoint
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
from level.goblin import Goblin
import pygame
from settings import TILE_SIZE

_GOBLIN_PREVIEW = None

def preview_goblin():
    global _GOBLIN_PREVIEW

    if _GOBLIN_PREVIEW is None:
        img = pygame.image.load("assets/goblin/1.png").convert_alpha()
        _GOBLIN_PREVIEW = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    return _GOBLIN_PREVIEW

def preview_player1():
    img = pygame.image.load("assets/hero/white_1.png").convert_alpha()
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

def preview_player2():
    img = pygame.image.load("assets/hero/black_1.png").convert_alpha()
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

# name, ascii, class, kwargs, rotatable
ENTITY_REGISTRY = [
    ("Tile", "#", Tile, {}, False, False),
    ("Ground", "@", Ground, {}, False, False),
    ("Left Wall", "l", LWall, {}, False, False),
    ("Right Wall", "r", RWall, {}, False, False),
    ("Left Corner", "L", LCorner, {}, False, False),
    ("Right Corner", "R", RCorner, {}, False, False),
    ("Left Drop", "(", LDrop, {}, False, False),
    ("Right Drop", ")", RDrop, {}, False, False),
    ("Downside", "u", Down, {}, False, False),
    ("Left Downside", "[", LDown, {}, False, False),
    ("Right Downside", "]", RDown, {}, False, False),
    ("Inner Left", "é", LInner, {}, False, False),
    ("Inner Right", "è", RInner, {}, False, False),
    ("Decoration", "/", Deco, {}, False, False),
    ("Push Block", "B", PushBlock, {}, False, False),
    ("Spike", "S", Spike, {}, False, False),
    ("Checkpoint", "C", Checkpoint, {}, False, False),
    ("Finish", "F", Finish, {}, False, False),
    ("Goblin", "G", None, {}, False, preview_goblin),
    ("Hold Plate", "p", HoldPlate, {"key": "A"}, False, False),
    ("Latch Plate", "P", LatchPlate, {"key": "B"}, False, False),
    ("Door OR", "d", Door, {"key": "A", "mode": "hold", "logic": "OR"}, False, False),
    ("Door AND", "D", Door, {"key": "B", "mode": "latch", "logic": "AND"}, False, False),


    ("Cannon >", ">", Cannon, {"direction": ">"}, True, False),

    ("Spawn P1", "1", None, {}, False, preview_player1),
    ("Spawn P2", "2", None, {}, False, preview_player2),
]
