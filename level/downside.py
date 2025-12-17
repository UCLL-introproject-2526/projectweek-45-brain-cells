import pygame
from core.entity import Entity

class Down(Entity):
    STONE_IMG = None
    STONE_DARK_IMG = None

    @classmethod
    def load_images(cls):
        if cls.STONE_IMG is None:
            cls.STONE_IMG = pygame.image.load(
                "assets/tiles/downside.png"
            ).convert_alpha()

            cls.STONE_DARK_IMG = pygame.image.load(
                "assets/tiles/stone_dark.png"
            ).convert_alpha()

    def __init__(self, x, y, size, variant=0):
        super().__init__(x, y, size, size)

        Down.load_images()

        self.variant = variant
        base_image = (
            Down.STONE_IMG if variant == 0 else Down.STONE_DARK_IMG
        )
        self.image = pygame.transform.scale(base_image, (size, size))

    def draw(self, surface, camera_offset=(0, 0)):
        surface.blit(
            self.image,
            (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        )

import pygame
from core.entity import Entity

class RDown(Entity):
    STONE_IMG = None
    STONE_DARK_IMG = None

    @classmethod
    def load_images(cls):
        if cls.STONE_IMG is None:
            cls.STONE_IMG = pygame.image.load(
                "assets/tiles/right_downside.png"
            ).convert_alpha()

            cls.STONE_DARK_IMG = pygame.image.load(
                "assets/tiles/stone_dark.png"
            ).convert_alpha()

    def __init__(self, x, y, size, variant=0):
        super().__init__(x, y, size, size)

        RDown.load_images()

        self.variant = variant
        base_image = (
            RDown.STONE_IMG if variant == 0 else RDown.STONE_DARK_IMG
        )
        self.image = pygame.transform.scale(base_image, (size, size))

    def draw(self, surface, camera_offset=(0, 0)):
        surface.blit(
            self.image,
            (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        )


import pygame
from core.entity import Entity

class LDown(Entity):
    STONE_IMG = None
    STONE_DARK_IMG = None

    @classmethod
    def load_images(cls):
        if cls.STONE_IMG is None:
            cls.STONE_IMG = pygame.image.load(
                "assets/tiles/left_downside.png"
            ).convert_alpha()

            cls.STONE_DARK_IMG = pygame.image.load(
                "assets/tiles/stone_dark.png"
            ).convert_alpha()

    def __init__(self, x, y, size, variant=0):
        super().__init__(x, y, size, size)

        LDown.load_images()

        self.variant = variant
        base_image = (
            LDown.STONE_IMG if variant == 0 else LDown.STONE_DARK_IMG
        )
        self.image = pygame.transform.scale(base_image, (size, size))

    def draw(self, surface, camera_offset=(0, 0)):
        surface.blit(
            self.image,
            (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        )

