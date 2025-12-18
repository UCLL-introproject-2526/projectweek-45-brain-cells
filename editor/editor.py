import pygame

class LevelEditor:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.want_exit = False

        self.font = pygame.font.SysFont(None, 32)

        # Example editor state
        self.camera_offset = pygame.Vector2(0, 0)

        # Button
        self.exit_rect = pygame.Rect(20, 20, 260, 50)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.want_exit = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_rect.collidepoint(event.pos):
                    self.want_exit = True

    def update(self, dt):
        self.handle_input()

    def draw(self):
        self.screen.fill((20, 20, 20))

        # --- Editor content placeholder ---
        grid_color = (50, 50, 50)
        for x in range(0, self.screen.get_width(), 64):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.screen.get_height()))
        for y in range(0, self.screen.get_height(), 64):
            pygame.draw.line(self.screen, grid_color, (0, y), (self.screen.get_width(), y))

        # --- Exit button ---
        pygame.draw.rect(self.screen, (80, 20, 20), self.exit_rect)
        label = self.font.render("Return to Main Menu", True, (255, 255, 255))
        label_rect = label.get_rect(center=self.exit_rect.center)
        self.screen.blit(label, label_rect)

        pygame.display.flip()
