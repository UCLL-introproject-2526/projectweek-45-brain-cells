import pygame
from core.entity import Entity
from settings import TILE_SIZE, GRAVITY


class PushBlock(Entity):
    # -------------------------
    # CLASS IMAGES
    # -------------------------
    STONE_IMG = None
    STONE_DARK_IMG = None

    @classmethod
    def load_images(cls):
        if cls.STONE_IMG is None:
            cls.STONE_IMG = pygame.image.load(
                "assets/pushblock.png"
            ).convert_alpha()

            cls.STONE_DARK_IMG = pygame.image.load(
                "assets/tiles/stone_dark.png"
            ).convert_alpha()

    # -------------------------
    # INIT
    # -------------------------
    def __init__(self, x, y, size=TILE_SIZE, variant=0):
        super().__init__(x, y, size, size)

        # physics
        self.vel = pygame.Vector2(0, 0)
        self.grabbed = False

        # graphics
        PushBlock.load_images()
        self.variant = variant

        base_image = (
            PushBlock.STONE_IMG if variant == 0
            else PushBlock.STONE_DARK_IMG
        )
        self.image = pygame.transform.scale(base_image, (size, size))

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, solids):
        # GRAVITY
        self.vel.y += GRAVITY

        # -------------------------
        # VERTICAL MOVE
        # -------------------------
        self.rect.y += int(self.vel.y)

        for s in solids:
            if self.rect.colliderect(s.rect):
                if self.vel.y > 0:  # falling
                    self.rect.bottom = s.rect.top
                    self.vel.y = 0
                elif self.vel.y < 0:  # jumping up
                    self.rect.top = s.rect.bottom
                    self.vel.y = 0

        # -------------------------
        # HORIZONTAL MOVE
        # -------------------------
        self.rect.x += int(self.vel.x)

        for s in solids:
            # only block sideways if overlapping vertically
            if self.rect.bottom > s.rect.top and self.rect.top < s.rect.bottom:
                if self.rect.colliderect(s.rect):
                    if self.vel.x > 0:
                        self.rect.right = s.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = s.rect.right

        # reset horizontal velocity
        self.vel.x = 0

    # -------------------------
    # DRAW
    # -------------------------
    def draw(self, surface, camera_offset=(0, 0)):
        surface.blit(
            self.image,
            (
                self.rect.x - camera_offset[0],
                self.rect.y - camera_offset[1]
            )
        )
