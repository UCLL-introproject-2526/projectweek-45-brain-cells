# editor/preview_cache.py
import pygame
from settings import TILE_SIZE


class PreviewCache:
    def __init__(self):
        self.cache = {}

    def _key(self, entry):
        _, ch, cls, _, _, _ = entry
        return ch

    def get(self, entry):
        key = self._key(entry)
        if key in self.cache:
            return self.cache[key]

        name, ch, cls, kwargs, _, preview_func = entry

        surf = pygame.Surface((64, 64), pygame.SRCALPHA)

        # -------------------------
        # CUSTOM PREVIEW FUNCTION
        # -------------------------
        if preview_func:
            img = preview_func()
            r = img.get_rect(center=(32, 32))
            surf.blit(img, r)

        # -------------------------
        # NORMAL ENTITY PREVIEW
        # -------------------------
        elif cls:
            try:
                obj = cls(0, 0, TILE_SIZE, **kwargs)
            except Exception:
                try:
                    obj = cls(0, 0, **kwargs)
                except Exception:
                    obj = None

            if obj:
                obj.rect.center = (32, 32)
                try:
                    obj.draw(surf, (0, 0))
                except Exception:
                    pygame.draw.rect(
                        surf, (120, 120, 120), (16, 16, 32, 32), 2
                    )

        self.cache[key] = surf
        return surf
