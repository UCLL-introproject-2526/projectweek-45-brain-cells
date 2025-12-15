import pygame

class LevelSelectMenu:
    def __init__(self, font):
        self.font = font
        self.visible = True
        self.selected = 0

        self._up_prev = False
        self._down_prev = False
        self._enter_prev = False
        self._esc_prev = False

    def open(self):
        self.visible = True

    def close(self):
        self.visible = False

    def handle_input(self, level_names):
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

        if up:
            self.selected = (self.selected - 1) % len(level_names)
        if down:
            self.selected = (self.selected + 1) % len(level_names)

        if esc:
            self.visible = False

        if enter and level_names:
            return self.selected

        return None

    def draw(self, surface, level_names, title="SELECT LEVEL"):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        w, h = surface.get_size()
        panel = pygame.Rect(w // 2 - 260, h // 2 - 220, 520, 440)
        pygame.draw.rect(surface, (40, 40, 60), panel, border_radius=12)
        pygame.draw.rect(surface, (10, 10, 20), panel, 3, border_radius=12)

        header = self.font.render(title, True, (240, 240, 255))
        surface.blit(header, (panel.centerx - header.get_width() // 2, panel.top + 20))

        y = panel.top + 90
        for i, name in enumerate(level_names):
            col = (255, 220, 120) if i == self.selected else (220, 220, 235)
            txt = self.font.render(name, True, col)
            surface.blit(txt, (panel.left + 40, y))
            y += 40

        hint = self.font.render("↑↓ select   Enter load   Esc close", True, (200, 200, 210))
        surface.blit(hint, (panel.centerx - hint.get_width() // 2, panel.bottom - 50))
