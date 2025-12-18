import pygame

def render_frame(state, surface, window):
    surface.fill((0, 0, 0))
    cam = state.camera.offset()

    state.level.draw_background(surface, cam, state.time)
    state.level.draw(surface, cam)

    if state.merged:
        state.merged.draw(surface, cam)
    else:
        state.player1.draw(surface, cam)
        state.player2.draw(surface, cam)

    for e in state.effects:
        e.draw(surface, cam)

    scaled = pygame.transform.scale(surface, window.get_size())
    window.blit(scaled, (0, 0))
    pygame.display.flip()
