import pygame
from core.entity import Entity
import random
from settings import TILE_SIZE
import os
from os import listdir

def load_deco_images():
    """Load all decoration images and return them as Surfaces."""
    images = []
    folder = "assets/deco"

    for file in os.listdir(folder):
        if file.endswith(".png"):
            image = pygame.image.load(
                os.path.join(folder, file)
            ).convert_alpha()
            images.append(image)

    return images


class Deco(Entity):
    IMAGES = []  # class-level cache

    @classmethod
    def load_images(cls):
        if cls.IMAGES:   # already loaded
            return
        cls.IMAGES = load_deco_images()

    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)

        Deco.load_images()

        # choose ONE random image per instance
        self.image = pygame.transform.scale(
            random.choice(Deco.IMAGES),
            (size, size)
        )

    def draw(self, surface, camera_offset=(0, 0)):
        surface.blit(
            self.image,
            (self.rect.x - camera_offset[0],
             self.rect.y - camera_offset[1])
        )