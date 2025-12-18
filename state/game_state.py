import pygame
from settings import *

from utils.input import PlayerInput
from players.player import Player

from ui.settings_menu import SettingsMenu
from ui.level_select_menu import LevelSelectMenu

from level.registry import discover_levels
from save.save_manager import load_save
from core.camera import Camera
from state.app_state import AppState
from ui.main_menu import MainMenu


from systems.input_building import build_inputs


class GameState:
    def __init__(self):
        # Window + render surface (same as your INIT)
        info = pygame.display.Info()
        self.WINDOW_WIDTH = info.current_w
        self.WINDOW_HIGHT = info.current_h

        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HIGHT),
            pygame.RESIZABLE
        )
        self.render_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("Split / Merge Dungeon")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.settings_menu = SettingsMenu(self.font)
        self.level_menu = LevelSelectMenu(self.font)
        self.effects = []

        self.app_state = AppState.MAIN_MENU

        self.main_menu = MainMenu(
            self.font,
            "assets/start_menu.png"   # ← your background image
)


        # SAVE DATA
        self.save_data = load_save()
        self.unlocked_levels = self.save_data.get("unlocked_levels", 1)

        # LEVELS
        self.level_classes = discover_levels("level.levels")
        self.level_names = [getattr(c, "name", c.__name__) for c in self.level_classes]

        # INPUTS
        self.p1_input, self.p2_input = build_inputs("QWERTY")

        # PLAYERS
        self.player1 = Player(120, 100, self.p1_input, "white")
        self.player2 = Player(200, 100, self.p2_input, "black")

        # MERGE STATE
        self.merged = None
        self.merge_cooldown = 0.0

        # MENU EDGE STATE (this is REQUIRED for popups)
        self.menu_key_prev = False
        self.level_key_prev = False

        # TIME / RUN
        self.t = 0.0
        self.running = True

        # LEVEL + CAMERA
        self.level = None
        self.camera = None

    def load_level(self, idx):
        # EXACT same load_level() you had
        self.merged = None
        self.level = self.level_classes[idx]()

        self.player1.rect.topleft = self.level.spawn_p1
        self.player2.rect.topleft = self.level.spawn_p2
        self.player1.vel.xy = (0, 0)
        self.player2.vel.xy = (0, 0)

        self.effects.clear()

        world_height = len(self.level.map_data) * TILE_SIZE
        self.camera = Camera(world_height)
