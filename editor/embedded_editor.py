import pygame
from settings import SCREEN_HEIGHT

from editor.editor_state import EditorState
from editor.camera import Camera
from editor.grid import Grid
from editor.hotbar import Hotbar
from editor.preview_cache import PreviewCache
from editor.tile_renderer import TileRenderer
from editor.entity_registry import ENTITY_REGISTRY
from editor.save_load import save_level
from editor.text_input import TextInput
from editor.background_picker import BackgroundPicker
from editor.rotation import rotate_char

from editor.dialogs.start_dialog import StartDialog
from editor.dialogs.new_level_dialog import NewLevelDialog
from editor.level_picker import LevelPicker
from editor.load_existing_level import load_level_into_editor
from editor.dialogs.pause_dialog import PauseDialog

import subprocess
import sys


class EmbeddedLevelEditor:
    """
    Runs your existing editor INSIDE an existing pygame screen.
    """

    def __init__(self, screen):
        self.screen = screen
        pygame.key.set_repeat(200, 60)

        self.font = pygame.font.SysFont(None, 28)

        # Return-to-menu button
        self.return_rect = pygame.Rect(16, 12, 260, 44)
        self.want_exit_to_menu = False

        # -------------------------
        # STARTUP STATE
        # -------------------------
        self.start_dialog = StartDialog(self.font)
        self.new_level_dialog = None
        self.level_picker = None

        self.state = None
        self.camera = None
        self.grid = None
        self.hotbar = None
        self.tile_renderer = None
        self.preview_cache = None
        self.pause_dialog = None

        self.dragging = False
        self.drag_anchor = None

        self.text_input = None
        self.bg_picker = None
        self.background_img = None

        # 🔑 TRACK WHICH LEVEL IS BEING EDITED
        self.editing_level_index = None

    # =========================================================
    # PLAYTEST
    # =========================================================
    def playtest(self):
        from editor.save_load import save_preview_level
        save_preview_level(self.state)
        subprocess.Popen([sys.executable, "main.py"])

    # =========================================================
    # TOP UI
    # =========================================================
    def _handle_return_button(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.return_rect.collidepoint(event.pos):
                self.want_exit_to_menu = True

    def _draw_return_button(self):
        pygame.draw.rect(self.screen, (20, 20, 20), self.return_rect, border_radius=8)
        pygame.draw.rect(self.screen, (220, 220, 220), self.return_rect, width=2, border_radius=8)
        label = self.font.render("Return to Main Menu", True, (255, 255, 255))
        self.screen.blit(label, label.get_rect(center=self.return_rect.center))

    # =========================================================
    # EVENT HANDLING
    # =========================================================
    def handle_events(self, events):
        for event in events:
            self._handle_return_button(event)

        # -------------------------
        # START DIALOG
        # -------------------------
        if self.start_dialog and self.start_dialog.active:
            for event in events:
                self.start_dialog.handle_event(event)
            return

        if self.start_dialog:
            if self.start_dialog.choice == "new":
                self.start_dialog = None
                self.new_level_dialog = NewLevelDialog(self.font)
                return

            if self.start_dialog.choice == "edit":
                self.start_dialog = None
                self.level_picker = LevelPicker(self.font)
                return

        # -------------------------
        # NEW LEVEL DIALOG
        # -------------------------
        if self.new_level_dialog and self.new_level_dialog.active:
            for event in events:
                self.new_level_dialog.handle_event(event)
            return

        if self.new_level_dialog and self.new_level_dialog.result:
            name, w, h = self.new_level_dialog.result

            self.state = EditorState(grid_w=w, grid_h=h)
            self.state.level_name = name

            self.editing_level_index = None  # 🔑 NEW LEVEL

            self.camera = Camera()
            self.grid = Grid(w, h)

            self.preview_cache = PreviewCache()
            self.hotbar = Hotbar(ENTITY_REGISTRY, self.preview_cache)
            self.tile_renderer = TileRenderer()

            self.new_level_dialog = None
            return

        # -------------------------
        # LEVEL PICKER
        # -------------------------
        if self.level_picker and self.level_picker.active:
            for event in events:
                self.level_picker.handle_event(event)
            return

        if self.level_picker and self.level_picker.selected is not None:
            self.editing_level_index = self.level_picker.selected

            self.state = load_level_into_editor(
                self.level_picker.selected,
                EditorState
            )

            self.camera = Camera()
            self.grid = Grid(len(self.state.map_data[0]), len(self.state.map_data))

            self.preview_cache = PreviewCache()
            self.hotbar = Hotbar(ENTITY_REGISTRY, self.preview_cache)
            self.tile_renderer = TileRenderer()

            self.level_picker = None
            return

        # -------------------------
        # PAUSE MENU
        # -------------------------
        if self.pause_dialog and self.pause_dialog.active:
            for event in events:
                self.pause_dialog.handle_event(event)
            return

        if self.pause_dialog and self.pause_dialog.choice:
            choice = self.pause_dialog.choice
            self.pause_dialog = None

            if choice == "resume":
                pass

            elif choice == "save":
                save_level(self.state, self.editing_level_index)

            elif choice == "save_&_exit":
                save_level(self.state, self.editing_level_index)
                self.state = None
                self.start_dialog = StartDialog(self.font)

            elif choice == "exit_without_saving":
                self.state = None
                self.start_dialog = StartDialog(self.font)

            return

        # -------------------------
        # NORMAL EDITOR LOOP
        # -------------------------
        if self.state is None:
            return

        for event in events:
            if self.hotbar:
                self.hotbar.handle_event(event)

            if self.text_input and self.text_input.active:
                result = self.text_input.handle_event(event)
                if result is not None:
                    self.state.level_name = result
                    self.text_input = None
                continue

            if self.bg_picker and self.bg_picker.active:
                result = self.bg_picker.handle_event(event)
                if result is not None:
                    self.state.background_path = result
                    try:
                        self.background_img = pygame.image.load(result).convert()
                    except Exception:
                        self.background_img = None
                    self.bg_picker = None
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    self.text_input = TextInput(self.font, "Level Name", self.state.level_name)

                elif event.key == pygame.K_ESCAPE:
                    self.pause_dialog = PauseDialog(self.font)

                elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.state.undo()

                elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.state.redo()

                elif event.key == pygame.K_p:
                    self.playtest()

                elif event.key == pygame.K_b:
                    self.bg_picker = BackgroundPicker(self.font)

                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_level(self.state, self.editing_level_index)

                elif event.key == pygame.K_r:
                    mx, my = pygame.mouse.get_pos()

                    if self.hotbar.rect(SCREEN_HEIGHT).collidepoint(mx, my):
                        continue

                    world = self.camera.screen_to_world(pygame.Vector2(mx, my))
                    cx, cy = self.grid.world_to_cell(world.x, world.y)

                    if self.state.in_bounds(cx, cy):
                        ch = self.state.map_data[cy][cx]

                        for entry in ENTITY_REGISTRY:
                            reg_ch = entry[1]
                            rotatable = entry[4]

                            if reg_ch == ch and rotatable:
                                new_ch = rotate_char(ch)
                                if new_ch != ch:
                                    self.state.snapshot()
                                    self.state.map_data[cy][cx] = new_ch
                                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if self.hotbar.rect(SCREEN_HEIGHT).collidepoint(mx, my):
                    idx = self.hotbar.tool_index_at(mx, my, SCREEN_HEIGHT)
                    if idx is not None:
                        self.state.selected_tool = idx
                    continue

                if not self.hotbar.dragging and (
                    event.button == 2 or
                    (event.button == 1 and pygame.key.get_pressed()[pygame.K_SPACE])
                ):
                    self.dragging = True
                    self.drag_anchor = pygame.Vector2(mx, my)
                    continue

                world = self.camera.screen_to_world(pygame.Vector2(mx, my))
                cx, cy = self.grid.world_to_cell(world.x, world.y)

                if self.state.in_bounds(cx, cy):
                    if event.button == 1:
                        _, ch, *_ = ENTITY_REGISTRY[self.state.selected_tool]
                        self.state.set_cell(cx, cy, ch)
                    elif event.button == 3:
                        self.state.clear_cell(cx, cy)

            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

    # =========================================================
    # UPDATE
    # =========================================================
    def update(self, dt):
        if self.dragging and self.camera:
            mx, my = pygame.mouse.get_pos()
            delta = self.drag_anchor - pygame.Vector2(mx, my)
            self.camera.move(delta.x, delta.y)
            self.drag_anchor.update(mx, my)

    # =========================================================
    # DRAW
    # =========================================================
    def draw(self):
        self.screen.fill((12, 12, 18))

        if self.start_dialog and self.start_dialog.active:
            self.start_dialog.draw(self.screen)
            self._draw_return_button()
            return

        if self.new_level_dialog and self.new_level_dialog.active:
            self.new_level_dialog.draw(self.screen)
            self._draw_return_button()
            return

        if self.level_picker and self.level_picker.active:
            self.level_picker.draw(self.screen)
            self._draw_return_button()
            return

        if self.pause_dialog and self.pause_dialog.active:
            self.pause_dialog.draw(self.screen)
            self._draw_return_button()
            return

        if self.state is None:
            self._draw_return_button()
            return

        self.tile_renderer.draw(self.screen, self.camera, self.state.map_data)
        self.grid.draw_lines(self.screen, self.camera)

        mx, my = pygame.mouse.get_pos()
        if not self.hotbar.rect(SCREEN_HEIGHT).collidepoint(mx, my):
            world = self.camera.screen_to_world(pygame.Vector2(mx, my))
            cx, cy = self.grid.world_to_cell(world.x, world.y)
            self.grid.draw_highlight(self.screen, self.camera, cx, cy)

        self.hotbar.draw(self.screen, self.state.selected_tool)
        self.hotbar.draw_tooltip(self.screen, mx, my, SCREEN_HEIGHT)

        if self.text_input and self.text_input.active:
            self.text_input.draw(self.screen)

        if self.bg_picker and self.bg_picker.active:
            self.bg_picker.draw(self.screen)

        self._draw_return_button()
