# editor/text_input.py
import pygame


class TextInput:
    def __init__(self, font, title, initial=""):
        self.font = font
        self.title = title
        self.text = initial
        self.active = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
                return self.text
            elif event.key == pygame.K_ESCAPE:
                self.active = False
                return None
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if event.unicode.isprintable():
                    self.text += event.unicode
        return None

    def draw(self, surface):
        w, h = surface.get_size()
        box = pygame.Rect(w // 2 - 200, h // 2 - 60, 400, 120)

        pygame.draw.rect(surface, (20, 20, 30), box)
        pygame.draw.rect(surface, (200, 200, 240), box, 2)

        title_surf = self.font.render(self.title, True, (220, 220, 235))
        text_surf = self.font.render(self.text + "|", True, (255, 255, 255))

        surface.blit(title_surf, (box.x + 10, box.y + 10))
        surface.blit(text_surf, (box.x + 10, box.y + 50))
