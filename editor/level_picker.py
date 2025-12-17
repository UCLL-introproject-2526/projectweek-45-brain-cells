import os
import pygame

LEVELS_DIR = "level/levels"


class LevelPicker:
    def __init__(self, font):
        self.font = font
        self.active = True
        self.selected = None

        self.levels = []
        for f in os.listdir(LEVELS_DIR):
            if f.startswith("level") and f.endswith(".py"):
                name = f[:-3]  # strip .py
                self.levels.append(name)

        self.index = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False

            elif event.key == pygame.K_UP:
                self.index = max(0, self.index - 1)

            elif event.key == pygame.K_DOWN:
                self.index = min(len(self.levels) - 1, self.index + 1)

            elif event.key == pygame.K_RETURN:
                level_name = self.levels[self.index]
                # ✅ RETURN FULL MODULE PATH
                self.selected = f"level.levels.{level_name}"
                self.active = False

    def draw(self, screen):
        screen.fill((20, 20, 30))

        title = self.font.render("Select Level to Edit", True, (220, 220, 220))
        screen.blit(title, (40, 30))

        for i, name in enumerate(self.levels):
            color = (255, 255, 255) if i == self.index else (140, 140, 140)
            txt = self.font.render(name, True, color)
            screen.blit(txt, (60, 80 + i * 28))
