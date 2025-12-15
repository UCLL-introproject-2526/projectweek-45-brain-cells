import pygame

class SettingsMenu:
    def __init__(self, font):
        self.font = font
        self.visible = False

        self.options = [
            "Keyboard Layout",
            "Volume",
            "Back"
        ]

        self.layouts = ["QWERTY", "AZERTY"]
        self.layout_index = 0

        self.volume = 80  # percent

        self.selected = 0

        self._up_prev = False
        self._down_prev = False
        self._left_prev = False
        self._right_prev = False
        self._enter_prev = False

    def toggle(self):
        self.visible = not self.visible

    def handle_input(self):
        keys = pygame.key.get_pressed()

        def pressed(key, prev):
            return keys[key] and not prev

        up = pressed(pygame.K_UP, self._up_prev)
        down = pressed(pygame.K_DOWN, self._down_prev)
        left = pressed(pygame.K_LEFT, self._left_prev)
        right = pressed(pygame.K_RIGHT, self._right_prev)
        enter = pressed(pygame.K_RETURN, self._enter_prev)

        self._up_prev = keys[pygame.K_UP]
        self._down_prev = keys[pygame.K_DOWN]
        self._left_prev = keys[pygame.K_LEFT]
        self._right_prev = keys[pygame.K_RIGHT]
        self._enter_prev = keys[pygame.K_RETURN]

        if up:
            self.selected = (self.selected - 1) % len(self.options)
        if down:
            self.selected = (self.selected + 1) % len(self.options)

        if self.options[self.selected] == "Keyboard Layout":
            if left or right:
                self.layout_index = (self.layout_index + 1) % len(self.layouts)

        elif self.options[self.selected] == "Volume":
            if left:
                self.volume = max(0, self.volume - 5)
            if right:
                self.volume = min(100, self.volume + 5)

        elif self.options[self.selected] == "Back":
            if enter:
                self.visible = False

    def draw(self, surface):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        w, h = surface.get_size()
        panel = pygame.Rect(w // 2 - 220, h // 2 - 160, 440, 320)
        pygame.draw.rect(surface, (40, 40, 60), panel, border_radius=10)
        pygame.draw.rect(surface, (10, 10, 20), panel, 3, border_radius=10)

        title = self.font.render("SETTINGS", True, (240, 240, 255))
        surface.blit(title, (panel.centerx - title.get_width() // 2, panel.top + 20))

        y = panel.top + 80
        for i, opt in enumerate(self.options):
            color = (255, 220, 120) if i == self.selected else (220, 220, 235)

            if opt == "Keyboard Layout":
                text = f"{opt}: {self.layouts[self.layout_index]}"
            elif opt == "Volume":
                text = f"{opt}: {self.volume}%"
            else:
                text = opt

            txt = self.font.render(text, True, color)
            surface.blit(txt, (panel.left + 40, y))
            y += 50
