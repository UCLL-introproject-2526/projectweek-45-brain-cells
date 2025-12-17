import pygame


class PauseDialog:
    def __init__(self, font):
        self.font = font
        self.active = True
        self.choice = None

        self.options = [
            "Resume",
            "Save",
            "Save & Exit",
            "Exit Without Saving",
        ]
        self.index = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.choice = "resume"
                self.active = False

            elif event.key == pygame.K_UP:
                self.index = max(0, self.index - 1)

            elif event.key == pygame.K_DOWN:
                self.index = min(len(self.options) - 1, self.index + 1)

            elif event.key == pygame.K_RETURN:
                opt = self.options[self.index]
                self.choice = opt.lower().replace(" ", "_")
                self.active = False

    def draw(self, screen):
        w, h = screen.get_size()

        # dark overlay
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # panel
        panel = pygame.Rect(w // 2 - 200, h // 2 - 140, 400, 280)
        pygame.draw.rect(screen, (30, 30, 45), panel)
        pygame.draw.rect(screen, (90, 90, 120), panel, 2)

        title = self.font.render("Paused", True, (230, 230, 230))
        screen.blit(title, (panel.centerx - title.get_width() // 2, panel.y + 20))

        for i, opt in enumerate(self.options):
            color = (255, 255, 255) if i == self.index else (160, 160, 160)
            txt = self.font.render(opt, True, color)
            screen.blit(txt, (panel.x + 80, panel.y + 80 + i * 36))
