import pygame
from core.entity import Entity
from settings import TILE_SIZE

class Checkpoint(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.active = False

        # Laad vlag-afbeeldingen
        self.img_inactive = pygame.image.load("assets/flags/flag_inactive.png").convert_alpha()
        self.img_active = pygame.image.load("assets/flags/flag_active.png").convert_alpha()

        # Optioneel: schaal ze naar TILE_SIZE
        self.img_inactive = pygame.transform.scale(self.img_inactive, (TILE_SIZE, TILE_SIZE))
        self.img_active = pygame.transform.scale(self.img_active, (TILE_SIZE, TILE_SIZE))

    def try_activate(self, merged, level):
        """
        Activeer checkpoint wanneer merged entity het raakt.
        Zet respawn-posities voor split players.
        """
        if self.active:
            return
        if merged and self.rect.colliderect(merged.rect):
            self.active = True

            level.respawn_p1 = (self.rect.centerx - 40, self.rect.bottom - 48)
            level.respawn_p2 = (self.rect.centerx + 40, self.rect.bottom - 48)

            # Optioneel: speel geluid
            # pygame.mixer.Sound("assets/sfx/checkpoint.wav").play()

    def draw(self, surface, cam):
        r = self.rect.move(-cam[0], -cam[1])
        img = self.img_active if self.active else self.img_inactive
        surface.blit(img, r)