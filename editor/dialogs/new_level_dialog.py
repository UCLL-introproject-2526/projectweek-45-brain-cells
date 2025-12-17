import pygame

class NewLevelDialog:
    def __init__(self, font):
        self.font = font
        self.active = True

        self.name = "New Level"
        self.width = "100"
        self.height = "40"
        self.focus = "name"

        self.result = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.focus = {"name": "width", "width": "height", "height": "name"}[self.focus]

            elif event.key == pygame.K_RETURN:
                self.result = (
                    self.name,
                    int(self.width),
                    int(self.height)
                )
                self.active = False

            elif event.key == pygame.K_BACKSPACE:
                self._backspace()
            else:
                self._type(event.unicode)

    def _type(self, char):
        if not char.isprintable():
            return
        if self.focus == "name":
            self.name += char
        elif self.focus == "width" and char.isdigit():
            self.width += char
        elif self.focus == "height" and char.isdigit():
            self.height += char

    def _backspace(self):
        if self.focus == "name":
            self.name = self.name[:-1]
        elif self.focus == "width":
            self.width = self.width[:-1]
        elif self.focus == "height":
            self.height = self.height[:-1]

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        box = pygame.Rect(180, 150, 440, 260)
        pygame.draw.rect(screen, (30, 30, 44), box, border_radius=8)

        def draw_field(label, value, y, active):
            color = (255, 255, 255) if active else (180, 180, 180)
            screen.blit(self.font.render(label, True, color), (220, y))
            pygame.draw.rect(screen, (70, 70, 100), (300, y - 4, 200, 32), 2)
            screen.blit(self.font.render(value, True, color), (308, y))

        draw_field("Name", self.name, 190, self.focus == "name")
        draw_field("Width", self.width, 240, self.focus == "width")
        draw_field("Height", self.height, 290, self.focus == "height")

        screen.blit(
            self.font.render("Press ENTER to create", True, (200, 200, 220)),
            (260, 340)
        )
