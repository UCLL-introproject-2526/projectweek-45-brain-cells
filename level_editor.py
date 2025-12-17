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
import subprocess
import sys


def playtest(state):
    from editor.save_load import save_preview_level

    save_preview_level(state)

    # launch the game as a subprocess
    subprocess.Popen([sys.executable, "main.py"])




def main():
    pygame.init()
    pygame.key.set_repeat(200, 60)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Level Editor")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    state = EditorState(grid_w=60, grid_h=20)
    camera = Camera()
    grid = Grid(state.grid_w, state.grid_h)

    preview_cache = PreviewCache()
    hotbar = Hotbar(ENTITY_REGISTRY, preview_cache)
    tile_renderer = TileRenderer()

    dragging = False
    drag_anchor = None

    text_input = None
    bg_picker = None
    background_img = None
    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            # -------------------------
            # QUIT
            # -------------------------
            if event.type == pygame.QUIT:
                running = False

            # -------------------------
            # POPUPS TAKE PRIORITY
            # -------------------------
            if text_input and text_input.active:
                result = text_input.handle_event(event)
                if result is not None:
                    state.level_name = result
                    text_input = None
                continue

            if bg_picker and bg_picker.active:
                result = bg_picker.handle_event(event)
                if result is not None:
                    state.background_path = result

                    # 🔑 LOAD BACKGROUND PREVIEW
                    try:
                        background_img = pygame.image.load(result).convert()
                    except Exception as e:
                        print("Failed to load background:", e)
                        background_img = None

                    bg_picker = None
                continue


            # -------------------------
            # KEY SHORTCUTS
            # -------------------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    text_input = TextInput(font, "Level Name", state.level_name)

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

                        for _, reg_ch, _, _, rotatable in ENTITY_REGISTRY:
                            if reg_ch == ch and rotatable:
                                new_ch = rotate_char(ch)

                                # 🔑 ONLY snapshot if something changes
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
                if event.button == 2 or (
                    event.button == 1 and pygame.key.get_pressed()[pygame.K_SPACE]
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
        # HOTBAR TOOLTIP
        mx, my = pygame.mouse.get_pos()
        hotbar.draw_tooltip(screen, mx, my, SCREEN_HEIGHT)


        # POPUPS
        if text_input and text_input.active:
            text_input.draw(screen)

        if bg_picker and bg_picker.active:
            bg_picker.draw(screen)
        # -------------------------
        # DRAW BACKGROUND PREVIEW
        # -------------------------
        # if background_img:
        #     cam_x, cam_y = camera.pos
        #     factor = 0.3  # parallax factor (matches game feel)

        #     screen.blit(
        #         background_img,
        #         (-cam_x * factor, -cam_y * factor)
        #     )


        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
