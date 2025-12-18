import pygame
from level.registry import load_all_levels, get_level_names


class LevelPicker:
    def __init__(self, font, background_path = "assets/start_menu.png"):
        # Big, clean font (reuse Cinzel if you want)
        self.font = pygame.font.Font("assets/Cinzel-Bold.ttf", 48)
        self.small_font = pygame.font.SysFont(None, 26)

        self.bg = pygame.image.load(background_path).convert_alpha()

        self.active = True
        self.selected = None  # will be an index

        # -------------------------
        # LOAD FROM levels.json
        # -------------------------
        self.levels_data = load_all_levels()
        self.levels = get_level_names(self.levels_data)

        self.index = 0

        # Edge-triggered input
        self._up_prev = False
        self._down_prev = False
        self._enter_prev = False
        self._esc_prev = False

        self.color_normal = (255, 255, 255)
        self.color_selected = (255, 215, 0)

    # =====================================================
    # INPUT
    # =====================================================
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

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
            self.index = (self.index - 1) % len(self.levels)

        elif down:
            self.index = (self.index + 1) % len(self.levels)

        elif enter:
            self.selected = self.index
            self.active = False

        elif esc:
            self.active = False

    # =====================================================
    # DRAW
    # =====================================================
    def draw(self, screen):
        w, h = screen.get_size()

        # -------------------------
        # BACKGROUND
        # -------------------------
        bg_scaled = pygame.transform.scale(self.bg, (w, h))
        screen.blit(bg_scaled, (0, 0))

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # -------------------------
        # TITLE
        # -------------------------
        title = self.font.render("SELECT LEVEL", True, (240, 240, 255))
        screen.blit(title, title.get_rect(center=(w // 2, h // 5)))

        # -------------------------
        # LEVEL LIST
        # -------------------------
        start_y = h // 3
        spacing = 56

        for i, name in enumerate(self.levels):
            color = self.color_selected if i == self.index else self.color_normal
            label = self.font.render(name, True, color)
            rect = label.get_rect(center=(w // 2, start_y + i * spacing))
            screen.blit(label, rect)

        # -------------------------
        # HINT
        # -------------------------
        hint = self.small_font.render(
            "↑ ↓ select    Enter edit    Esc back",
            True,
            (200, 200, 210)
        )
        screen.blit(hint, hint.get_rect(center=(w // 2, h - 50)))
