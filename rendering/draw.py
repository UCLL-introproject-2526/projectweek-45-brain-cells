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
