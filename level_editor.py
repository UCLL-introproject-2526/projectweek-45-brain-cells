import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

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


# =========================================================
# PLAYTEST
# =========================================================
def playtest(state):
    from editor.save_load import save_preview_level
    save_preview_level(state)
    subprocess.Popen([sys.executable, "main.py"])


# =========================================================
# MAIN
# =========================================================
def main():
    pygame.init()
    pygame.key.set_repeat(200, 60)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Level Editor")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    # -------------------------
    # STARTUP STATE
    # -------------------------
    start_dialog = StartDialog(font)
    new_level_dialog = None
    level_picker = None

    state = None
    camera = None
    grid = None
    hotbar = None
    tile_renderer = None
    preview_cache = None
    pause_dialog = None

    dragging = False
    drag_anchor = None

    text_input = None
    bg_picker = None
    background_img = None

    running = True
    while running:
        clock.tick(60)

        # =================================================
        # START DIALOG
        # =================================================
        if start_dialog and start_dialog.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                start_dialog.handle_event(event)

            start_dialog.draw(screen)
            pygame.display.flip()
            continue

        if start_dialog:
            if start_dialog.choice == "new":
                start_dialog = None
                new_level_dialog = NewLevelDialog(font)
                continue

            if start_dialog.choice == "edit":
                start_dialog = None
                level_picker = LevelPicker(font)
                continue

        # =================================================
        # NEW LEVEL DIALOG
        # =================================================
        if new_level_dialog and new_level_dialog.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                new_level_dialog.handle_event(event)

            new_level_dialog.draw(screen)
            pygame.display.flip()
            continue

        if new_level_dialog and new_level_dialog.result:
            name, w, h = new_level_dialog.result

            state = EditorState(grid_w=w, grid_h=h)
            state.level_name = name

            camera = Camera()
            grid = Grid(w, h)

            preview_cache = PreviewCache()
            hotbar = Hotbar(ENTITY_REGISTRY, preview_cache)
            tile_renderer = TileRenderer()

            new_level_dialog = None

        # =================================================
        # LEVEL PICKER (EDIT EXISTING)
        # =================================================
        if level_picker and level_picker.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                level_picker.handle_event(event)

            level_picker.draw(screen)
            pygame.display.flip()
            continue

        if level_picker and level_picker.selected:
            state = load_level_into_editor(
                level_picker.selected,
                EditorState
            )

            camera = Camera()
            grid = Grid(len(state.map_data[0]), len(state.map_data))

            preview_cache = PreviewCache()
            hotbar = Hotbar(ENTITY_REGISTRY, preview_cache)
            tile_renderer = TileRenderer()

            level_picker = None

        # =================================================
        # PAUSE MENU
        # =================================================
        if pause_dialog and pause_dialog.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                pause_dialog.handle_event(event)

            pause_dialog.draw(screen)
            pygame.display.flip()
            continue

        if pause_dialog and pause_dialog.choice:
            choice = pause_dialog.choice
            pause_dialog = None

            if choice == "resume":
                pass

            elif choice == "save":
                save_level(state)

            elif choice == "save_&_exit":
                save_level(state)
                state = None
                start_dialog = StartDialog(font)

            elif choice == "exit_without_saving":
                state = None
                start_dialog = StartDialog(font)


        # =================================================
        # NORMAL EDITOR LOOP
        # =================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            hotbar.handle_event(event)

            # -------------------------
            # TEXT INPUT POPUP
            # -------------------------
            if text_input and text_input.active:
                result = text_input.handle_event(event)
                if result is not None:
                    state.level_name = result
                    text_input = None
                continue

            # -------------------------
            # BACKGROUND PICKER
            # -------------------------
            if bg_picker and bg_picker.active:
                result = bg_picker.handle_event(event)
                if result is not None:
                    state.background_path = result
                    try:
                        background_img = pygame.image.load(result).convert()
                    except Exception:
                        background_img = None
                    bg_picker = None
                continue

            # -------------------------
            # KEYBOARD SHORTCUTS
            # -------------------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    text_input = TextInput(font, "Level Name", state.level_name)

                elif event.key == pygame.K_ESCAPE:
                    pause_dialog = PauseDialog(font)


                elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    state.undo()

                elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    state.redo()

                elif event.key == pygame.K_p:
                    playtest(state)

                elif event.key == pygame.K_b:
                    bg_picker = BackgroundPicker(font)

                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_level(state)

                elif event.key == pygame.K_r:
                    mx, my = pygame.mouse.get_pos()

                    # ignore hotbar
                    if hotbar.rect(SCREEN_HEIGHT).collidepoint(mx, my):
                        continue

                    world = camera.screen_to_world(pygame.Vector2(mx, my))
                    cx, cy = grid.world_to_cell(world.x, world.y)

                    if state.in_bounds(cx, cy):
                        ch = state.map_data[cy][cx]

                        for entry in ENTITY_REGISTRY:
                            reg_ch = entry[1]
                            rotatable = entry[4]

                            if reg_ch == ch and rotatable:
                                new_ch = rotate_char(ch)

                                if new_ch != ch:
                                    state.snapshot()
                                    state.map_data[cy][cx] = new_ch
                                break

            # -------------------------
            # MOUSE INPUT
            # -------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # HOTBAR
                if hotbar.rect(SCREEN_HEIGHT).collidepoint(mx, my):
                    idx = hotbar.tool_index_at(mx, my, SCREEN_HEIGHT)
                    if idx is not None:
                        state.selected_tool = idx
                    continue

                # CAMERA DRAG
                if not hotbar.dragging and (
                    event.button == 2 or
                    (event.button == 1 and pygame.key.get_pressed()[pygame.K_SPACE])
                ):

                    dragging = True
                    drag_anchor = pygame.Vector2(mx, my)
                    continue

                # PLACE / ERASE
                world = camera.screen_to_world(pygame.Vector2(mx, my))
                cx, cy = grid.world_to_cell(world.x, world.y)

                if state.in_bounds(cx, cy):
                    if event.button == 1:
                        _, ch, *_ = ENTITY_REGISTRY[state.selected_tool]
                        state.set_cell(cx, cy, ch)
                    elif event.button == 3:
                        state.clear_cell(cx, cy)

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

        # -------------------------
        # CAMERA DRAG
        # -------------------------
        if dragging:
            mx, my = pygame.mouse.get_pos()
            delta = drag_anchor - pygame.Vector2(mx, my)
            camera.move(delta.x, delta.y)
            drag_anchor.update(mx, my)

        # -------------------------
        # DRAW
        # -------------------------
        screen.fill((12, 12, 18))

        tile_renderer.draw(screen, camera, state.map_data)
        grid.draw_lines(screen, camera)

        mx, my = pygame.mouse.get_pos()
        if not hotbar.rect(SCREEN_HEIGHT).collidepoint(mx, my):
            world = camera.screen_to_world(pygame.Vector2(mx, my))
            cx, cy = grid.world_to_cell(world.x, world.y)
            grid.draw_highlight(screen, camera, cx, cy)

        hotbar.draw(screen, state.selected_tool)
        hotbar.draw_tooltip(screen, mx, my, SCREEN_HEIGHT)

        if text_input and text_input.active:
            text_input.draw(screen)

        if bg_picker and bg_picker.active:
            bg_picker.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
