import pygame
from settings import MENU_MUSIC, GAME_MUSIC


def play_music(path, volume):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)


def ensure_music(state, target):
    """
    target: "menu" or "game"
    """
    if state.current_music == target:
        return

    if target == "menu":
        play_music(MENU_MUSIC, state.settings_menu.volume / 100.0)
    elif target == "game":
        play_music(GAME_MUSIC, state.settings_menu.volume / 100.0)

    state.current_music = target
