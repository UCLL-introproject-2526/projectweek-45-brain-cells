import pygame

class StartDialog:
    def __init__(self, font):
        self.font = font
        self.choice = None
        self.active = True

        self.btn_new = pygame.Rect(260, 220, 280, 50)
        self.btn_edit = pygame.Rect(260, 290, 280, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_new.collidepoint(event.pos):
                self.choice = "new"
                self.active = False
            elif self.btn_edit.collidepoint(event.pos):
                self.choice = "edit"
                self.active = False

    def draw(self, screen):
        screen.fill((18, 18, 28))

        title = self.font.render("LEVEL EDITOR", True, (220, 220, 240))
        screen.blit(title, title.get_rect(center=(400, 160)))

        pygame.draw.rect(screen, (50, 50, 70), self.btn_new, border_radius=8)
        pygame.draw.rect(screen, (50, 50, 70), self.btn_edit, border_radius=8)

        screen.blit(
            self.font.render("Create New Level", True, (240, 240, 255)),
            self.btn_new.move(40, 12)
        )
        screen.blit(
            self.font.render("Edit Existing Level", True, (240, 240, 255)),
            self.btn_edit.move(25, 12)
        )
