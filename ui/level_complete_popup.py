import pygame


class LevelCompletePopup:
    def __init__(self, font_big, font_small, time_sec, best_time, is_new_record):
        self.font_big = font_big
        self.font_small = font_small

        self.time_sec = time_sec
        self.best_time = best_time
        self.is_new_record = is_new_record

        self.visible = True
        self.clicked_continue = False

        self.button_rect = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect and self.button_rect.collidepoint(event.pos):
                self.clicked_continue = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.clicked_continue = True

    def draw(self, surface):
        w, h = surface.get_size()

        # dark overlay
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        # panel
        panel = pygame.Rect(w // 2 - 260, h // 2 - 200, 520, 400)
        pygame.draw.rect(surface, (40, 40, 60), panel, border_radius=14)
        pygame.draw.rect(surface, (10, 10, 20), panel, 3, border_radius=14)

        # title
        title = self.font_big.render("LEVEL COMPLETE", True, (255, 255, 255))
        surface.blit(
            title,
            title.get_rect(center=(panel.centerx, panel.top + 50))
        )

        # time formatting
        def fmt(t):
            m = int(t // 60)
            s = t % 60
            return f"{m:02}:{s:05.2f}"

        # your time
        your_time = self.font_small.render(
            f"Your Time: {fmt(self.time_sec)}",
            True,
            (230, 230, 230)
        )
        surface.blit(
            your_time,
            your_time.get_rect(center=(panel.centerx, panel.top + 140))
        )

        # best time
        if self.best_time is None:
            best_txt = "Best Time: --:--.--"
        else:
            best_txt = f"Best Time: {fmt(self.best_time)}"

        best_time = self.font_small.render(best_txt, True, (200, 200, 200))
        surface.blit(
            best_time,
            best_time.get_rect(center=(panel.centerx, panel.top + 180))
        )

        # new record
        if self.is_new_record:
            record = self.font_small.render(
                "NEW HIGH SCORE!",
                True,
                (255, 220, 120)
            )
            surface.blit(
                record,
                record.get_rect(center=(panel.centerx, panel.top + 220))
            )

        # continue button
        self.button_rect = pygame.Rect(
            panel.centerx - 120,
            panel.bottom - 90,
            240,
            50
        )

        pygame.draw.rect(surface, (80, 120, 80), self.button_rect, border_radius=10)
        pygame.draw.rect(surface, (20, 20, 20), self.button_rect, 2, border_radius=10)

        btn = self.font_small.render("Continue", True, (255, 255, 255))
        surface.blit(
            btn,
            btn.get_rect(center=self.button_rect.center)
        )
