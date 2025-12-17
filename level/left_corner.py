import pygame
from core.entity import Entity

class LCorner(Entity):
    STONE_IMG = None
    STONE_DARK_IMG = None

    @classmethod
    def load_images(cls):
        if cls.STONE_IMG is None:
            cls.STONE_IMG = pygame.image.load(
                "assets/tiles/left_corner.png"
            ).convert_alpha()

            cls.STONE_DARK_IMG = pygame.image.load(
                "assets/tiles/stone_dark.png"
            ).convert_alpha()

    def __init__(self, x, y, size, variant=0):
        super().__init__(x, y, size, size)

        LCorner.load_images()

        self.variant = variant
        base_image = (
            LCorner.STONE_IMG if variant == 0 else LCorner.STONE_DARK_IMG
        )
        self.image = pygame.transform.scale(base_image, (size, size))

    def draw(self, surface, camera_offset=(0, 0)):
        surface.blit(
            self.image,
            (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        )

