import pygame


class MainMenu:
    def __init__(self, font, background_path):
        # 🔹 Use a BIGGER font for menu items
        self.font = pygame.font.Font("assets/Cinzel-Bold.ttf", 72)

        self.bg = pygame.image.load(background_path).convert_alpha()

        self.options = ["Play", "Create Level", "Quit"]
        self.selected = 0

        # Colors
        self.color_normal = (255, 255, 255)   # white
        self.color_selected = (255, 215, 0)   # yellow/gold

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.selected = (self.selected - 1) % len(self.options)
            pygame.time.wait(150)

        if keys[pygame.K_DOWN]:
            self.selected = (self.selected + 1) % len(self.options)
            pygame.time.wait(150)

        if keys[pygame.K_RETURN]:
            return self.options[self.selected]

        return None

    def draw(self, screen):
        # -------------------------
        # BACKGROUND
        # -------------------------
        bg_scaled = pygame.transform.scale(self.bg, screen.get_size())
        screen.blit(bg_scaled, (0, 0))

        # -------------------------
        # MENU TEXT
        # -------------------------
        w, h = screen.get_size()
        start_y = h // 3

        for i, text in enumerate(self.options):
            color = self.color_selected if i == self.selected else self.color_normal

            label = self.font.render(text, True, color)
            rect = label.get_rect(center=(w // 2, start_y + i * 80))
            screen.blit(label, rect)
