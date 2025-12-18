from level.ascii_level import AsciiLevel
from settings import TILE_SIZE


class JsonLevel(AsciiLevel):
    def __init__(self, level_data):
        self.name = level_data["name"]
        raw_map = level_data["map_data"]

        # -------------------------------------------------
        # TEMP map for spawn detection
        # -------------------------------------------------
        map_rows = [list(row) for row in raw_map]

        spawn_p1 = None
        spawn_p2 = None

        for y, row in enumerate(map_rows):
            for x, ch in enumerate(row):
                if ch == "1":
                    spawn_p1 = (x * TILE_SIZE, y * TILE_SIZE)
                    map_rows[y][x] = "."
                elif ch == "2":
                    spawn_p2 = (x * TILE_SIZE, y * TILE_SIZE)
                    map_rows[y][x] = "."

        # final cleaned map
        self.map_data = ["".join(row) for row in map_rows]

        # -------------------------------------------------
        # LET AsciiLevel BUILD EVERYTHING
        # -------------------------------------------------
        super().__init__()

        # -------------------------------------------------
        # OVERRIDE SPAWNS (IMPORTANT)
        # -------------------------------------------------
        if spawn_p1 is None or spawn_p2 is None:
            raise ValueError(
                f"Level '{self.name}' must contain spawn tiles '1' and '2'"
            )

        self.spawn_p1 = spawn_p1
        self.spawn_p2 = spawn_p2

        self.respawn_p1 = spawn_p1
        self.respawn_p2 = spawn_p2

        # -------------------------------------------------
        # BACKGROUND
        # -------------------------------------------------
        bg = level_data.get("background")
        if bg:
            self.load_background(bg)
