import pygame


class Hotbar:
    def __init__(self, registry, preview_cache):
        self.registry = registry
        self.preview_cache = preview_cache

        self.icon_size = 48
        self.padding = 8
        self.margin = 8

        # scrolling
        self.scroll_x = 0
        self.dragging = False
        self.drag_start_x = 0
        self.scroll_start_x = 0

    # --------------------------------------------------
    # GEOMETRY
    # --------------------------------------------------
    def rect(self, screen_h):
        return pygame.Rect(
            0,
            screen_h - self.icon_size - self.margin * 2,
            pygame.display.get_surface().get_width(),
            self.icon_size + self.margin * 2
        )

    def total_width(self):
        return len(self.registry) * (self.icon_size + self.padding)

    # --------------------------------------------------
    # INPUT
    # --------------------------------------------------
    def handle_event(self, event):
        screen = pygame.display.get_surface()
        if not screen:
            return

        bar_rect = self.rect(screen.get_height())

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if bar_rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_start_x = event.pos[0]
                self.scroll_start_x = self.scroll_x

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            dx = event.pos[0] - self.drag_start_x
            self.scroll_x = self.scroll_start_x + dx

            max_scroll = 0
            min_scroll = min(0, screen.get_width() - self.total_width())
            self.scroll_x = max(min_scroll, min(max_scroll, self.scroll_x))

    # --------------------------------------------------
    # TOOL SELECTION
    # --------------------------------------------------
    def tool_index_at(self, mx, my, screen_h):
        bar_rect = self.rect(screen_h)
        if not bar_rect.collidepoint(mx, my):
            return None

        local_x = mx - self.scroll_x
        idx = local_x // (self.icon_size + self.padding)

        if 0 <= idx < len(self.registry):
            return int(idx)

        return None

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------
    def draw(self, surface, selected_index):
        bar_rect = self.rect(surface.get_height())

        # hotbar background
        pygame.draw.rect(surface, (24, 24, 34), bar_rect)
        pygame.draw.rect(surface, (60, 60, 90), bar_rect, 2)

        y = bar_rect.y + self.margin

        for i, entry in enumerate(self.registry):
            x = self.scroll_x + i * (self.icon_size + self.padding)

            # cull offscreen icons
            if x + self.icon_size < 0 or x > bar_rect.width:
                continue

            icon_rect = pygame.Rect(x, y, self.icon_size, self.icon_size)

            # slot background
            pygame.draw.rect(surface, (32, 32, 46), icon_rect)

            # slot border
            border_col = (120, 140, 220) if i == selected_index else (70, 70, 100)
            pygame.draw.rect(surface, border_col, icon_rect, 2)

            # draw preview centered
            preview = self.preview_cache.get(entry)
            if preview:
                pr = preview.get_rect(center=icon_rect.center)
                surface.blit(preview, pr)


    # --------------------------------------------------
    # TOOLTIP
    # --------------------------------------------------
    def draw_tooltip(self, surface, mx, my, screen_h):
        idx = self.tool_index_at(mx, my, screen_h)
        if idx is None:
            return

        name = self.registry[idx][0]
        font = pygame.font.SysFont(None, 20)

        text = font.render(name, True, (240, 240, 240))
        padding = 6

        rect = text.get_rect()
        rect.topleft = (mx + 12, my - rect.height - 12)

        bg = pygame.Rect(
            rect.x - padding,
            rect.y - padding,
            rect.width + padding * 2,
            rect.height + padding * 2
        )

        pygame.draw.rect(surface, (20, 20, 30), bg)
        pygame.draw.rect(surface, (80, 80, 110), bg, 1)

        surface.blit(text, rect)
