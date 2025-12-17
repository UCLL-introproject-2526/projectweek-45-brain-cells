# editor/background_picker.py
import os
import pygame


class BackgroundPicker:
    def __init__(self, font, folder="assets/Backdrops"):
        self.font = font
        self.folder = folder
        self.files = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        self.index = 0
        self.active = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
                return self.files[self.index] if self.files else ""
            elif event.key == pygame.K_ESCAPE:
                self.active = False
                return None
            elif event.key == pygame.K_LEFT:
                self.index = (self.index - 1) % len(self.files)
            elif event.key == pygame.K_RIGHT:
                self.index = (self.index + 1) % len(self.files)
        return None

    def draw(self, surface):
        w, h = surface.get_size()
        box = pygame.Rect(w // 2 - 220, h // 2 - 160, 440, 320)

        pygame.draw.rect(surface, (20, 20, 30), box)
        pygame.draw.rect(surface, (200, 200, 240), box, 2)

        title = self.font.render("Pick Background (← →, Enter)", True, (220, 220, 235))
        surface.blit(title, (box.x + 10, box.y + 10))

        if not self.files:
            msg = self.font.render("No images found", True, (200, 100, 100))
            surface.blit(msg, (box.centerx - msg.get_width() // 2, box.centery))
            return

        img = pygame.image.load(self.files[self.index]).convert()
        img = pygame.transform.scale(img, (400, 200))
        surface.blit(img, (box.x + 20, box.y + 60))
