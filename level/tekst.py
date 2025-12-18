import pygame
from core.entity import Entity

class T1(Entity):
    STONE_IMG = None
    STONE_DARK_IMG = None

    @classmethod
    def load_images(cls):
        if cls.STONE_IMG is None:
            cls.STONE_IMG = pygame.image.load(
                "assets/tekst/Tekst.png"
            ).convert_alpha()

            cls.STONE_DARK_IMG = pygame.image.load(
                "assets/tiles/stone_dark.png"
            ).convert_alpha()

    def __init__(self, x, y, size, variant=0):
        super().__init__(x, y, size, size)

        T1.load_images()

        self.variant = variant
        base_image = (
            T1.STONE_IMG if variant == 0 else T1.STONE_DARK_IMG
        )
        self.image = pygame.transform.scale(base_image, (size, size))

    def draw(self, surface, camera_offset=(0, 0)):
        surface.blit(
            self.image,
            (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        )

import pygame
from core.entity import Entity

class T2(Entity):
    STONE_IMG = None
    STONE_DARK_IMG = None

    @classmethod
    def load_images(cls):
        if cls.STONE_IMG is None:
            cls.STONE_IMG = pygame.image.load(
                "assets/tekst/T2.png"
            ).convert_alpha()

            cls.STONE_DARK_IMG = pygame.image.load(
                "assets/tiles/stone_dark.png"
            ).convert_alpha()

    def __init__(self, x, y, size, variant=0):
        super().__init__(x, y, size, size)

        T2.load_images()

        self.variant = variant
        base_image = (
            T2.STONE_IMG if variant == 0 else T2.STONE_DARK_IMG
        )
        self.image = pygame.transform.scale(base_image, (size, size))

    def draw(self, surface, camera_offset=(0, 0)):
        surface.blit(
            self.image,
            (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        )


import pygame
from core.entity import Entity

class T3(Entity):
    STONE_IMG = None
    STONE_DARK_IMG = None

    @classmethod
    def load_images(cls):
        if cls.STONE_IMG is None:
            cls.STONE_IMG = pygame.image.load(
                "assets/tekst/T3.png"
            ).convert_alpha()

            cls.STONE_DARK_IMG = pygame.image.load(
                "assets/tiles/stone_dark.png"
            ).convert_alpha()

    def __init__(self, x, y, size, variant=0):
        super().__init__(x, y, size, size)

        T3.load_images()

        self.variant = variant
        base_image = (
            T3.STONE_IMG if variant == 0 else T3.STONE_DARK_IMG
        )
        self.image = pygame.transform.scale(base_image, (size, size))

    def draw(self, surface, camera_offset=(0, 0)):
        surface.blit(
            self.image,
            (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        )

class T4(Entity):
    STONE_IMG = None
    STONE_DARK_IMG = None

    @classmethod
    def load_images(cls):
        if cls.STONE_IMG is None:
            cls.STONE_IMG = pygame.image.load(
                "assets/tekst/T4.png"
            ).convert_alpha()

            cls.STONE_DARK_IMG = pygame.image.load(
                "assets/tiles/stone_dark.png"
            ).convert_alpha()

    def __init__(self, x, y, size, variant=0):
        super().__init__(x, y, size, size)

        T4.load_images()

        self.variant = variant
        base_image = (
            T4.STONE_IMG if variant == 0 else T4.STONE_DARK_IMG
        )
        self.image = pygame.transform.scale(base_image, (size, size))

    def draw(self, surface, camera_offset=(0, 0)):
        surface.blit(
            self.image,
            (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        )