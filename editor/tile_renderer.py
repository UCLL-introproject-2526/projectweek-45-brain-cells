# editor/tile_renderer.py
import pygame
from settings import TILE_SIZE
from editor.entity_registry import ENTITY_REGISTRY


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
        name, ch, cls, kwargs, _ = entry
        if cls is None:
            return None

        try:
            return cls(0, 0, **kwargs)
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

                ent = self.get_entity(ch)
                if not ent:
                    continue

                ent.rect.topleft = (
                    cx * TILE_SIZE - camera.pos.x,
                    cy * TILE_SIZE - camera.pos.y
                )

                ent.draw(surface, (0, 0))
