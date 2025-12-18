import pygame

def draw_actors(state, surface, cam):
    if state.merged:
        state.merged.draw(surface, cam)
    else:
        state.player1.draw(surface, cam)
        state.player2.draw(surface, cam)

def draw_world(state, surface, cam):
    state.level.draw_background(surface, cam, state.t)
    state.level.draw(surface, cam)
    draw_actors(state, surface, cam)


def blit_scaled(state):
    scaled = pygame.transform.scale(
        state.render_surface,
        state.screen.get_size()
    )
    state.screen.blit(scaled, (0, 0))
    pygame.display.flip()

def draw_timer(surface, state):
    """
    Draws the current level timer and best time.
    """
    # BIG current time font
    big_font = state.font_big
    small_font = state.font_small

    # -------------------------
    # CURRENT TIME
    # -------------------------
    t = state.level_time
    minutes = int(t // 60)
    seconds = t % 60
    time_text = f"{minutes:02}:{seconds:05.2f}"

    label = big_font.render(time_text, True, (255, 255, 255))
    rect = label.get_rect(midtop=(surface.get_width() // 2, 16))
    surface.blit(label, rect)

    # -------------------------
    # BEST TIME
    # -------------------------
    level_data = state.levels_data[state.level_index]
    best = level_data.get("best_time")

    if best is None:
        best_text = "Best: --:--.--"
    else:
        m = int(best // 60)
        s = best % 60
        best_text = f"Best: {m:02}:{s:05.2f}"

    best_label = small_font.render(best_text, True, (200, 200, 200))
    best_rect = best_label.get_rect(
        midtop=(surface.get_width() // 2, rect.bottom + 4)
    )
    surface.blit(best_label, best_rect)
