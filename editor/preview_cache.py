# editor/preview_cache.py
import pygame
from settings import TILE_SIZE


class PreviewCache:
    def __init__(self):
        self.cache = {}

    def _key(self, entry):
        _, ch, cls, _, _ = entry
        return (ch, cls)

    def get(self, entry):
        key = self._key(entry)
        if key in self.cache:
            return self.cache[key]

        name, ch, cls, kwargs, _ = entry
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)

        if cls:
            try:
                obj = cls(0, 0, **kwargs)
                obj.rect.topleft = (16, 16)
                obj.draw(surf, (0, 0))
            except Exception:
                pygame.draw.rect(surf, (120, 120, 120), (16, 16, 32, 32), 2)

        self.cache[key] = surf
        return surf
