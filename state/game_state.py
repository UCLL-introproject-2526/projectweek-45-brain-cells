import pygame
from settings import *

from utils.input import PlayerInput
from players.player import Player

from ui.settings_menu import SettingsMenu
from ui.level_select_menu import LevelSelectMenu
from ui.main_menu import MainMenu

from save.save_manager import load_save
from core.camera import Camera
from state.app_state import AppState

from systems.input_building import build_inputs

# JSON level system
from level.registry import load_all_levels, get_level_names, load_level


class GameState:
    def __init__(self):
        self.level_complete_popup = None

                # -------------------------
        # TIMER FONTS
        # -------------------------
        self.font_big = pygame.font.SysFont(None, 64)    # BIG timer
        self.font_small = pygame.font.SysFont(None, 28)  # Best time

        # -------------------------
        # WINDOW + RENDER SURFACE
        # -------------------------
        info = pygame.display.Info()
        self.WINDOW_WIDTH = info.current_w
        self.WINDOW_HIGHT = info.current_h
        # -------------------------
        # LEVEL TIMER
        # -------------------------
        self.level_time = 0.0
        self.level_timer_running = False

        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HIGHT),
            pygame.RESIZABLE
        )
        self.render_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("Split / Merge Dungeon")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        # -------------------------
        # MENUS
        # -------------------------
        self.settings_menu = SettingsMenu(self.font)
        self.level_menu = LevelSelectMenu(self.font)

        self.app_state = AppState.MAIN_MENU

        self.main_menu = MainMenu(
            self.font,
            "assets/start_menu.png"
        )

        # -------------------------
        # SAVE DATA
        # -------------------------
        self.save_data = load_save()
        self.unlocked_levels = self.save_data.get("unlocked_levels", 1)

        # -------------------------
        # LEVEL DATA (FROM levels.json)
        # -------------------------
        self.levels_data = load_all_levels()
        self.level_names = get_level_names(self.levels_data)

        # -------------------------
        # INPUTS
        # -------------------------
        self.p1_input, self.p2_input = build_inputs("QWERTY")

        # -------------------------
        # PLAYERS
        # -------------------------
        self.player1 = Player(120, 100, self.p1_input, "white")
        self.player2 = Player(200, 100, self.p2_input, "black")

        # -------------------------
        # MERGE STATE
        # -------------------------
        self.merged = None
        self.merge_cooldown = 0.0

        # -------------------------
        # MENU EDGE STATE
        # -------------------------
        self.menu_key_prev = False
        self.level_key_prev = False

        # -------------------------
        # EFFECTS / TIME / RUN
        # -------------------------
        self.effects = []
        self.t = 0.0
        self.running = True

        # -------------------------
        # LEVEL + CAMERA
        # -------------------------
        self.level = None
        self.camera = None

        # -------------------------
        # EMBEDDED EDITOR
        # -------------------------
        self.editor = None

    # =====================================================
    # LOAD LEVEL (JSON-BASED)
    # =====================================================
    def load_level(self, idx):
        self.level_index = idx   # 👈 store index for record saving
        self.level = load_level(idx, self.levels_data)

        self.merged = None

        self.player1.rect.topleft = self.level.spawn_p1
        self.player2.rect.topleft = self.level.spawn_p2
        self.player1.vel.xy = (0, 0)
        self.player2.vel.xy = (0, 0)

        self.effects.clear()

        world_height = len(self.level.map_data) * TILE_SIZE
        self.camera = Camera(world_height)

        # ⏱ TIMER RESET
        self.level_time = 0.0
        self.level_timer_running = True

