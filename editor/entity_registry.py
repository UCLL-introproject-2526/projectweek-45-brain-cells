# editor/entity_registry.py

from level.tile import Tile
from level.obstacle import PushBlock
from level.spikes import Spike
from level.cannon import Cannon
from level.devices import Door, Finish, HoldPlate, LatchPlate
from level.checkpoint import Checkpoint

# name, ascii, class, kwargs, rotatable
ENTITY_REGISTRY = [
    ("Tile", "#", Tile, {}, False),
    ("Push Block", "B", PushBlock, {}, False),
    ("Spike", "S", Spike, {}, False),
    ("Checkpoint", "C", Checkpoint, {}, False),
    ("Finish", "F", Finish, {}, False),

    ("Hold Plate", "p", HoldPlate, {"key": "A"}, False),
    ("Latch Plate", "P", LatchPlate, {"key": "B"}, False),

    ("Door AND", "D", Door, {"key": "B", "mode": "latch", "logic": "AND"}, False),
    ("Door OR", "d", Door, {"key": "A", "mode": "hold", "logic": "OR"}, False),

    ("Cannon >", ">", Cannon, {"direction": ">"}, True),
    ("Cannon <", "<", Cannon, {"direction": "<"}, True),
    ("Cannon ^", "^", Cannon, {"direction": "^"}, True),
    ("Cannon v", "v", Cannon, {"direction": "v"}, True),

    ("Spawn P1", "1", None, {}, False),
    ("Spawn P2", "2", None, {}, False),
]
