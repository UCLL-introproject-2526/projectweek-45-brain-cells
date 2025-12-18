import pygame
from utils.input import PlayerInput

def build_inputs(layout):
    layout = layout.upper()

    if layout == "QWERTY":
        p1 = PlayerInput(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_e)
    elif layout == "AZERTY":
        p1 = PlayerInput(pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_e)
    else:
        raise ValueError(f"Unknown keyboard layout: {layout}")

    p2 = PlayerInput(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_RSHIFT)
    return p1, p2
