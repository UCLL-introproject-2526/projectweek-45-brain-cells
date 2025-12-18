import pygame
from core.entity import Entity
from settings import TILE_SIZE

class Switch(Entity):
    """
    On when a player or block is standing on it.
    """
    def __init__(self, x, y, w=48, h=12, key="A"):
        super().__init__(x, y, w, h)
        self.key = key
        self.on = False

    def update(self, dt, actors):
        self.on = False
        for a in actors:
            feet = pygame.Rect(
                a.rect.left + 6,
                a.rect.bottom - 4,
                a.rect.width - 12,
                6
            )
            if feet.colliderect(self.rect):
                self.on = True
                break

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        color = (60, 210, 90) if self.on else (170, 60, 60)
        pygame.draw.rect(surface, color, r)
        pygame.draw.rect(surface, (20, 20, 20), r, 2)

def resolve_overlap(rect, obstacle_rect):
    """
    Gently push rect out of obstacle_rect using minimal axis resolution.
    """
    dx_left = obstacle_rect.right - rect.left
    dx_right = rect.right - obstacle_rect.left
    dy_top = obstacle_rect.bottom - rect.top
    dy_bottom = rect.bottom - obstacle_rect.top

    min_overlap = min(dx_left, dx_right, dy_top, dy_bottom)

    if min_overlap == dx_left:
        rect.left = obstacle_rect.right
    elif min_overlap == dx_right:
        rect.right = obstacle_rect.left
    elif min_overlap == dy_top:
        rect.top = obstacle_rect.bottom
    else:
        rect.bottom = obstacle_rect.top


class Door:
    def __init__(self, x, y, w, h, key, mode="hold", logic="AND"):
        self.rect = pygame.Rect(x, y, w, h)
        self.key = key
        self.mode = mode
        self.logic = logic
        self.open = False
        self._was_open = False   # 🔑 track state change

        self.image = pygame.image.load("assets/tiles/brick_wall.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (w, h))

    @property
    def solid(self):
        return not self.open

    def update(self, plates, actors=None):
        self._was_open = self.open

        linked = [p for p in plates if p.key == self.key]
        if not linked:
            return

        if self.logic == "AND":
            self.open = all(p.active for p in linked)
        elif self.logic == "OR":
            self.open = any(p.active for p in linked)

        # 🔑 Door just CLOSED
        if self._was_open and not self.open and actors:
            for a in actors:
                if self.rect.colliderect(a.rect):
                    resolve_overlap(a.rect, self.rect)


    def draw(self, surface, cam):
        if self.open:
            return

        r = self.rect.move(-cam[0], -cam[1])
        surface.blit(self.image, r)




class Finish(Entity):
    def __init__(self, x, y, w=64, h=96, variant = 0):
        super().__init__(x, y, w, h)
        Finish.load_images()
        self.variant = variant
        base_image = (
            Finish.STONE_IMG if variant == 0 else Finish.STONE_DARK_IMG
        )
        self.image = pygame.transform.scale(base_image, (w, h))
    STONE_IMG = None
    STONE_DARK_IMG = None

    @classmethod
    def load_images(cls):
        if cls.STONE_IMG is None:
            cls.STONE_IMG = pygame.image.load(
                "assets/tiles/Finish.png"
            ).convert_alpha()

            cls.STONE_DARK_IMG = pygame.image.load(
                "assets/tiles/stone_dark.png"
            ).convert_alpha()        

    def draw(self, surface, camera_offset=(0, 0)):
        surface.blit(
            self.image,
            (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        )


class PressurePlate:
    def __init__(self, x, y, key):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE/4)
        self.key = key
        self.active = False

    def update(self, actors):
        self.active = any(self.rect.colliderect(a.rect) for a in actors)

    def draw(self, surface, cam):
        r = self.rect.move(-cam[0], -cam[1])
        color = (200, 80, 80) if self.active else (120, 40, 40)
        pygame.draw.rect(surface, color, r)



class LatchPlate(PressurePlate):
    def __init__(self, x, y, key):
        super().__init__(x, y, key)
        self.triggered = False

    def update(self, actors):
        if not self.triggered:
            super().update(actors)
            if self.active:
                self.triggered = True
                self.active = True
        else:
            self.active = True


class HoldPlate(PressurePlate):
    pass
