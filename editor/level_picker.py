import pygame
from level.registry import load_all_levels, get_level_names


class LevelPicker:
    def __init__(self, font):
        self.font = font
        self.active = True
        self.selected = None  # will be an index

        # -------------------------
        # LOAD FROM levels.json
        # -------------------------
        self.levels_data = load_all_levels()
        self.levels = get_level_names(self.levels_data)

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
                # ✅ RETURN LEVEL INDEX
                self.selected = self.index
                self.active = False

    def draw(self, screen):
        screen.fill((20, 20, 30))

        title = self.font.render("Select Level to Edit", True, (220, 220, 220))
        screen.blit(title, (40, 30))

        for i, name in enumerate(self.levels):
            color = (255, 255, 255) if i == self.index else (140, 140, 140)
            txt = self.font.render(name, True, color)
            screen.blit(txt, (60, 80 + i * 28))

        hint = self.font.render(
            "Enter: edit    Esc: cancel",
            True,
            (120, 120, 120)
        )
        screen.blit(hint, (40, screen.get_height() - 40))
