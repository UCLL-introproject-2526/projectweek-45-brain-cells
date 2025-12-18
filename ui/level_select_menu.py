import pygame


class LevelSelectMenu:
    def __init__(self, font):
        self.font = font
        self.visible = True
        self.selected = 0

        # scrolling
        self.scroll_offset = 0
        self.row_height = 40
        self.visible_rows = 7

        # input edge tracking
        self._up_prev = False
        self._down_prev = False
        self._enter_prev = False
        self._esc_prev = False

        # button rect (calculated in draw)
        self.return_button = None

    def open(self):
        self.visible = True

    def close(self):
        self.visible = False

    # -------------------------------------------------
    # INPUT
    # -------------------------------------------------
    def handle_input(self, level_names, unlocked_count):
        keys = pygame.key.get_pressed()

        def pressed(key, prev):
            return keys[key] and not prev

        up = pressed(pygame.K_UP, self._up_prev)
        down = pressed(pygame.K_DOWN, self._down_prev)
        enter = pressed(pygame.K_RETURN, self._enter_prev)
        esc = pressed(pygame.K_ESCAPE, self._esc_prev)

        self._up_prev = keys[pygame.K_UP]
        self._down_prev = keys[pygame.K_DOWN]
        self._enter_prev = keys[pygame.K_RETURN]
        self._esc_prev = keys[pygame.K_ESCAPE]

        # keyboard navigation
        if up:
            self.selected = max(0, self.selected - 1)
        if down:
            self.selected = min(len(level_names) - 1, self.selected + 1)

        # auto-scroll to keep selection visible
        if self.selected < self.scroll_offset:
            self.scroll_offset = self.selected
        elif self.selected >= self.scroll_offset + self.visible_rows:
            self.scroll_offset = self.selected - self.visible_rows + 1

        if esc:
            return "MAIN_MENU"

        if enter and self.selected < unlocked_count:
            return self.selected

        return None

    # -------------------------------------------------
    # MOUSE INPUT
    # -------------------------------------------------
    def handle_event(self, event, level_names):
        # mouse wheel scrolling
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y
            self.scroll_offset = max(
                0,
                min(self.scroll_offset, max(0, len(level_names) - self.visible_rows))
            )

        # return to menu button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.return_button and self.return_button.collidepoint(event.pos):
                return "MAIN_MENU"

        return None

    # -------------------------------------------------
    # DRAW
    # -------------------------------------------------
    def draw(self, surface, level_names, unlocked_count):
        # dark overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        w, h = surface.get_size()
        panel = pygame.Rect(w // 2 - 260, h // 2 - 260, 520, 520)
        pygame.draw.rect(surface, (40, 40, 60), panel, border_radius=12)
        pygame.draw.rect(surface, (10, 10, 20), panel, 3, border_radius=12)

        # title
        title = self.font.render("SELECT LEVEL", True, (240, 240, 255))
        surface.blit(
            title,
            (panel.centerx - title.get_width() // 2, panel.top + 20)
        )

        # -------------------------
        # LEVEL LIST (SCROLLABLE)
        # -------------------------
        start_y = panel.top + 80
        end_index = min(
            len(level_names),
            self.scroll_offset + self.visible_rows
        )

        y = start_y
        for i in range(self.scroll_offset, end_index):
            name = level_names[i]
            locked = i >= unlocked_count

            color = (
                (120, 120, 120) if locked
                else ((255, 220, 120) if i == self.selected else (220, 220, 235))
            )

            label = name if not locked else f"{name} (LOCKED)"
            txt = self.font.render(label, True, color)
            surface.blit(txt, (panel.left + 40, y))

            y += self.row_height

        # -------------------------
        # SCROLL BAR (visual cue)
        # -------------------------
        if len(level_names) > self.visible_rows:
            bar_height = int(
                (self.visible_rows / len(level_names)) * (self.visible_rows * self.row_height)
            )
            bar_y = start_y + int(
                (self.scroll_offset / len(level_names)) * (self.visible_rows * self.row_height)
            )

            scrollbar = pygame.Rect(panel.right - 20, bar_y, 6, bar_height)
            pygame.draw.rect(surface, (160, 160, 180), scrollbar, border_radius=3)

        # -------------------------
        # RETURN TO MAIN MENU BUTTON
        # -------------------------
        self.return_button = pygame.Rect(
            panel.centerx - 140,
            panel.bottom - 80,
            280,
            44
        )

        pygame.draw.rect(surface, (70, 20, 20), self.return_button, border_radius=8)
        pygame.draw.rect(surface, (180, 180, 180), self.return_button, 2, border_radius=8)

        btn_text = self.font.render("Return to Main Menu", True, (255, 255, 255))
        surface.blit(
            btn_text,
            btn_text.get_rect(center=self.return_button.center)
        )

        # hint
        hint = self.font.render(
            "↑↓ select   Enter load   Mouse Wheel scroll   Esc back",
            True,
            (200, 200, 210)
        )
        surface.blit(
            hint,
            (panel.centerx - hint.get_width() // 2, panel.bottom - 25)
        )
