# editor/hotbar.py
import pygame


class Hotbar:
    def __init__(self, tools, preview_cache, height=96):
        self.tools = tools
        self.preview_cache = preview_cache
        self.height = height

        self.slot_size = 64
        self.padding = 12
        self.spacing = 8

        self.font = pygame.font.SysFont(None, 20)

    def rect(self, screen_height):
        return pygame.Rect(
            0,
            screen_height - self.height,
            pygame.display.get_surface().get_width(),
            self.height,
        )

    def tool_index_at(self, mx, my, screen_height):
        y0 = screen_height - self.height
        x = self.padding

        for i in range(len(self.tools)):
            slot = pygame.Rect(x, y0 + 16, self.slot_size, self.slot_size)
            if slot.collidepoint(mx, my):
                return i
            x += self.slot_size + self.spacing
        return None

    def hovered_tool(self, mx, my, screen_height):
        return self.tool_index_at(mx, my, screen_height)

    def draw(self, surface, selected_index):
        screen_w, screen_h = surface.get_size()
        y0 = screen_h - self.height

        pygame.draw.rect(surface, (18, 18, 26), (0, y0, screen_w, self.height))
        pygame.draw.line(surface, (80, 80, 110), (0, y0), (screen_w, y0), 2)

        x = self.padding
        for i, entry in enumerate(self.tools):
            slot = pygame.Rect(x, y0 + 16, self.slot_size, self.slot_size)

            pygame.draw.rect(surface, (30, 30, 44), slot, border_radius=6)
            pygame.draw.rect(
                surface,
                (200, 200, 240) if i == selected_index else (80, 80, 110),
                slot,
                2,
                border_radius=6,
            )

            preview = self.preview_cache.get(entry)
            surface.blit(preview, slot)

            x += self.slot_size + self.spacing

    # -------------------------
    # TOOLTIP
    # -------------------------
    def draw_tooltip(self, surface, mx, my, screen_height):
        idx = self.hovered_tool(mx, my, screen_height)
        if idx is None:
            return

        name = self.tools[idx][0]
        text = self.font.render(name, True, (240, 240, 250))

        padding = 6
        box = text.get_rect()
        box.topleft = (mx + 12, my - box.height - 12)
        bg = pygame.Rect(
            box.x - padding,
            box.y - padding,
            box.width + padding * 2,
            box.height + padding * 2,
        )

        pygame.draw.rect(surface, (20, 20, 30), bg, border_radius=6)
        pygame.draw.rect(surface, (160, 160, 200), bg, 1, border_radius=6)
        surface.blit(text, box)
