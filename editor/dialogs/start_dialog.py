import pygame


class StartDialog:
    def __init__(self, font, background_image="assets/start_menu.png"):
        self.font = pygame.font.Font("assets/Cinzel-Bold.ttf", 56)
        self.choice = None
        self.active = True

        self.background = pygame.image.load(background_image).convert_alpha()

        self.options = ["Create New Level", "Edit Existing Level"]
        self.selected = 0

        # colors
        self.color_normal = (255, 255, 255)
        self.color_selected = (255, 215, 0)

        # keyboard edge tracking
        self._up_prev = False
        self._down_prev = False
        self._enter_prev = False

        # mouse rects (positioned dynamically)
        self.btn_new = pygame.Rect(0, 0, 0, 0)
        self.btn_edit = pygame.Rect(0, 0, 0, 0)

    # =====================================================
    # INPUT
    # =====================================================
    def handle_event(self, event):
        # ---------- Mouse ----------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_new.collidepoint(event.pos):
                self.choice = "new"
                self.active = False
            elif self.btn_edit.collidepoint(event.pos):
                self.choice = "edit"
                self.active = False

        # ---------- Keyboard ----------
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            def pressed(key, prev):
                return keys[key] and not prev

            up = pressed(pygame.K_UP, self._up_prev)
            down = pressed(pygame.K_DOWN, self._down_prev)
            enter = pressed(pygame.K_RETURN, self._enter_prev)

            self._up_prev = keys[pygame.K_DOWN]
            self._down_prev = keys[pygame.K_UP]
            self._enter_prev = keys[pygame.K_RETURN]

            if up:
                self.selected = (self.selected - 1) % len(self.options)

            if down:
                self.selected = (self.selected + 1) % len(self.options)

            if enter:
                self.choice = "new" if self.selected == 0 else "edit"
                self.active = False

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

        # dark overlay
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # -------------------------
        # TITLE
        # -------------------------
        title_font = pygame.font.Font("assets/Cinzel-Bold.ttf", 64)
        title = title_font.render("LEVEL EDITOR", True, (240, 240, 255))
        screen.blit(title, title.get_rect(center=(w // 2, h // 3 - 80)))

        # -------------------------
        # OPTIONS
        # -------------------------
        start_y = h // 3
        spacing = 80

        for i, text in enumerate(self.options):
            color = self.color_selected if i == self.selected else self.color_normal
            label = self.font.render(text, True, color)

            rect = label.get_rect(center=(w // 2, start_y + i * spacing))
            screen.blit(label, rect)

            # update mouse hitboxes
            if i == 0:
                self.btn_new = rect.inflate(40, 20)
            else:
                self.btn_edit = rect.inflate(40, 20)
