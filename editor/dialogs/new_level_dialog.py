import pygame


class NewLevelDialog:
    def __init__(self, font, background_image="assets/start_menu.png"):
        self.font = font
        self.title_font = pygame.font.Font("assets/Cinzel-Bold.ttf", 48)

        self.background = pygame.image.load(background_image).convert_alpha()

        self.active = True
        self.result = None

        self.fields = {
            "name": "New Level",
            "width": "100",
            "height": "40",
        }

        self.order = ["name", "width", "height"]
        self.focus_index = 0

        self.color_normal = (220, 220, 235)
        self.color_selected = (255, 215, 0)
        self.box_color = (60, 60, 90)

        self._up_prev = False
        self._down_prev = False
        self._enter_prev = False

        self.boxes = {}

    # =====================================================
    # INPUT
    # =====================================================
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            def pressed(key, prev):
                return keys[key] and not prev

            up = pressed(pygame.K_UP, self._up_prev)
            down = pressed(pygame.K_DOWN, self._down_prev)
            enter = pressed(pygame.K_RETURN, self._enter_prev)

            self._up_prev = keys[pygame.K_UP]
            self._down_prev = keys[pygame.K_DOWN]
            self._enter_prev = keys[pygame.K_RETURN]

            if up:
                self.focus_index = (self.focus_index - 1) % len(self.order)
                return

            if down:
                self.focus_index = (self.focus_index + 1) % len(self.order)
                return

            if enter:
                try:
                    self.result = (
                        self.fields["name"].strip() or "New Level",
                        int(self.fields["width"]),
                        int(self.fields["height"]),
                    )
                    self.active = False
                except ValueError:
                    pass
                return

            if event.key == pygame.K_BACKSPACE:
                key = self.order[self.focus_index]
                self.fields[key] = self.fields[key][:-1]
                return

            char = event.unicode
            key = self.order[self.focus_index]

            if not char.isprintable():
                return

            if key == "name":
                self.fields[key] += char
            elif char.isdigit():
                self.fields[key] += char

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, key in enumerate(self.order):
                if key in self.boxes and self.boxes[key].collidepoint(event.pos):
                    self.focus_index = i
                    break

    # =====================================================
    # DRAW
    # =====================================================
    def draw(self, screen):
        w, h = screen.get_size()

        # -------------------------
        # BACKGROUND
        # -------------------------
        if self.background:
            bg = pygame.transform.scale(self.background, (w, h))
            screen.blit(bg, (0, 0))
        else:
            screen.fill((15, 15, 25))

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # -------------------------
        # PANEL
        # -------------------------
        panel_w, panel_h = 520, 360
        panel = pygame.Rect(
            (w - panel_w) // 2,
            (h - panel_h) // 2,
            panel_w,
            panel_h
        )

        pygame.draw.rect(screen, (30, 30, 44), panel, border_radius=12)
        pygame.draw.rect(screen, (15, 15, 25), panel, 3, border_radius=12)

        title = self.title_font.render("CREATE NEW LEVEL", True, (240, 240, 255))
        screen.blit(title, title.get_rect(center=(panel.centerx, panel.top + 40)))

        start_y = panel.top + 100
        spacing = 70
        box_w, box_h = 280, 40

        self.boxes.clear()

        for i, key in enumerate(self.order):
            y = start_y + i * spacing
            active = i == self.focus_index

            color = self.color_selected if active else self.color_normal

            screen.blit(
                self.font.render(key.capitalize(), True, color),
                (panel.left + 40, y + 6)
            )

            box = pygame.Rect(panel.left + 180, y, box_w, box_h)
            self.boxes[key] = box

            pygame.draw.rect(screen, self.box_color, box, border_radius=6)
            pygame.draw.rect(screen, color, box, 2, border_radius=6)

            txt = self.font.render(self.fields[key], True, color)
            screen.blit(
                txt,
                (box.x + 10, box.y + (box_h - txt.get_height()) // 2)
            )

        hint = self.font.render(
            "↑ ↓ navigate   Enter create",
            True,
            (180, 180, 200)
        )
        screen.blit(hint, hint.get_rect(center=(panel.centerx, panel.bottom - 30)))
