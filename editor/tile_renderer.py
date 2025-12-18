# editor/tile_renderer.py
import pygame
from settings import TILE_SIZE
from editor.entity_registry import ENTITY_REGISTRY, preview_goblin, preview_player1, preview_player2




class TileRenderer:
    """
    Renders ASCII map data using real entity sprites.
    Entities are created ONLY for drawing.
    """

    def __init__(self):
        # map ascii -> registry entry
        self.registry = {entry[1]: entry for entry in ENTITY_REGISTRY}
        self.cache = {}

    def _make_entity(self, entry):
        name, ch, cls, kwargs, *_ = entry
        if cls is None:
            return None

        try:
            return cls(0, 0, **kwargs)
        except Exception:
            try:
                return cls(0, 0, TILE_SIZE, **kwargs)
            except Exception:
                return None

    def get_entity(self, ch):
        if ch in self.cache:
            return self.cache[ch]

        entry = self.registry.get(ch)
        if not entry:
            return None

        ent = self._make_entity(entry)
        self.cache[ch] = ent
        return ent

    def draw(self, surface, camera, map_data):
        for cy, row in enumerate(map_data):
            for cx, ch in enumerate(row):
                if ch == " ":
                    continue

                px = cx * TILE_SIZE - camera.pos.x
                py = cy * TILE_SIZE - camera.pos.y

                # -------------------------
                # GOBLIN PREVIEW (SPECIAL)
                # -------------------------
                if ch == "G":
                    surface.blit(preview_goblin(), (px, py))
                    continue

                # -------------------------
                # PLAYER PREVIEWS (SPECIAL)
                if ch == "1":
                    surface.blit(preview_player1(), (px, py))
                    continue
                if ch == "2":
                    surface.blit(preview_player2(), (px, py))
                    continue
                # -------------------------
                # NORMAL ENTITIES
                # -------------------------
                ent = self.get_entity(ch)
                if not ent:
                    continue

                ent.rect.topleft = (px, py)
                ent.draw(surface, (0, 0))


