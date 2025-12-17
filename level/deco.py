import pygame
from core.entity import Entity
import random
import pygame
from settings import TILE_SIZE
import os
from os import listdir

def random_deco():# get the path/directory
    image_list = []
    folder_dir = "assets/deco"
    for images in os.listdir(folder_dir):

        # check if the image ends with png
        if (images.endswith(".png")):
            image_list.append(images)
    
    return image_list
            


class Deco(Entity):
    STONE_IMG = None
    STONE_DARK_IMG = None

    @classmethod
    def load_images(cls):
        for i in random_deco():
            if cls.STONE_IMG is None:
                cls.STONE_IMG = pygame.image.load(
                    f"assets/deco/{i}"
                ).convert_alpha()

                cls.STONE_DARK_IMG = pygame.image.load(
                    "assets/tiles/stone_dark.png"
                ).convert_alpha()

    def __init__(self, x, y, size, variant=0):
        super().__init__(x, y, size, size)
        self.images = random_deco()

        Deco.load_images()

        self.variant = variant
        base_image = (
            Deco.STONE_IMG if variant == 0 else Deco.STONE_DARK_IMG
        )
        self.image = pygame.transform.scale(base_image, (size, size))

    def draw(self, surface, camera_offset=(0, 0)):
        
        surface.blit(
            pygame.image.load(f"assets/deco/{random.choice(self.images)}").convert_alpha(),
            (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        )