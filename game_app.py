import asyncio
import pygame

from state.game_state import GameState
from state.app_state import AppState
from systems.gameplay import update_gameplay
from systems.effects import update_effects
from rendering.draw import draw_world
from editor.embedded_editor import EmbeddedLevelEditor
from systems.input_building import build_inputs  # top of file or local import
from rendering.draw import draw_timer
from systems.audio import ensure_music

class GameApp:
    def __init__(self):
        self.state = GameState()

    def run(self):
        s = self.state

        while s.running:
            dt = s.clock.tick(60) / 1000.0
            s.t += dt

            # -------------------------------------------------
            # COLLECT EVENTS ONCE
            # -------------------------------------------------
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    s.running = False

            # =====================================================
            # MAIN MENU
            # =====================================================
            if s.app_state == AppState.MAIN_MENU:
                ensure_music(s, "menu")
                choice = s.main_menu.handle_input()

                if choice == "Play":
                    s.level_menu.open()
                    s.load_level(0)
                    s.app_state = AppState.PLAYING

                elif choice == "Create Level":
                    s.editor = None
                    s.app_state = AppState.LEVEL_EDITOR

                elif choice == "Quit":
                    s.running = False

                s.main_menu.draw(s.screen)
                pygame.display.flip()
                continue

            # =====================================================
            # LEVEL EDITOR (EMBEDDED, SAME WINDOW)
            # =====================================================
            if s.app_state == AppState.LEVEL_EDITOR:
                if s.editor is None:
                    s.editor = EmbeddedLevelEditor(s.screen, s)

                s.editor.handle_events(events)
                s.editor.update(dt)
                s.editor.draw()
                pygame.display.flip()

                if s.editor.want_exit_to_menu:
                    s.editor = None
                    s.app_state = AppState.MAIN_MENU

                continue

            # =====================================================
            # PLAY MODE
            # =====================================================
            s.render_surface.fill((0, 0, 0))

            keys = pygame.key.get_pressed()

            # Menu toggles (edge-triggered)
            if keys[pygame.K_m] and not s.menu_key_prev:
                s.settings_menu.toggle()
                s.level_menu.visible = False
            s.menu_key_prev = keys[pygame.K_m]

            if keys[pygame.K_l] and not s.level_key_prev:
                s.level_menu.open()
                s.settings_menu.visible = False
            s.level_key_prev = keys[pygame.K_l]

            s.camera.update(
                [s.merged.rect] if s.merged else [s.player1.rect, s.player2.rect]
            )
            cam = s.camera.offset()

            # =====================================================
            # LEVEL SELECT MENU (UPDATED)
            # =====================================================
            if s.level_menu.visible:
                ensure_music(s, "menu")
                # mouse + button handling
                for event in events:
                    result = s.level_menu.handle_event(event, s.level_names)
                    if result == "MAIN_MENU":
                        s.level_menu.close()
                        s.app_state = AppState.MAIN_MENU

                # keyboard handling
                choice = s.level_menu.handle_input(
                    s.level_names, s.unlocked_levels
                )

                if isinstance(choice, int):
                    s.load_level(choice)
                    s.level_menu.close()

                draw_world(s, s.render_surface, cam)

                scaled = pygame.transform.scale(
                    s.render_surface, s.screen.get_size()
                )
                s.screen.blit(scaled, (0, 0))

                s.level_menu.draw(
                    s.screen, s.level_names, s.unlocked_levels
                )

                pygame.display.flip()
                continue

            # =====================================================
            # SETTINGS MENU
            # =====================================================
            if s.settings_menu.visible:
                ensure_music(s, "menu")
                s.settings_menu.handle_input()

                pygame.mixer.music.set_volume(
        s.settings_menu.volume / 100.0
    )

                if s.settings_menu.layout_changed:
                    s.p1_input, s.p2_input = build_inputs(
                        s.settings_menu.layouts[s.settings_menu.layout_index]
                    )
                    s.p1_input.reset()
                    s.p2_input.reset()

                    s.player1.input = s.p1_input
                    s.player2.input = s.p2_input

                    # if you're currently merged, update merged inputs too (safe)
                    if s.merged is not None:
                        if hasattr(s.merged, "p1_input"):
                            s.merged.p1_input = s.p1_input
                        if hasattr(s.merged, "p2_input"):
                            s.merged.p2_input = s.p2_input
                        if hasattr(s.merged, "input1"):
                            s.merged.input1 = s.p1_input
                        if hasattr(s.merged, "input2"):
                            s.merged.input2 = s.p2_input

                    s.settings_menu.layout_changed = False


                pygame.mixer.music.set_volume(
                    s.settings_menu.volume / 100.0
                )

                draw_world(s, s.render_surface, cam)

                scaled = pygame.transform.scale(
                    s.render_surface, s.screen.get_size()
                )
                s.screen.blit(scaled, (0, 0))

                s.settings_menu.draw(s.screen)

                pygame.display.flip()
                continue

            # ---------------- LEVEL COMPLETE POPUP ----------------
            if s.level_complete_popup:
                ensure_music(s, "menu")
                for event in events:
                    s.level_complete_popup.handle_event(event)

                s.level_complete_popup.draw(s.screen)
                pygame.display.flip()

                if s.level_complete_popup.clicked_continue:
                    s.level_complete_popup = None
                    s.level_menu.open()

                continue


            # =====================================================
            # GAMEPLAY
            # =====================================================
            # ---------------- TIMER ----------------
            if s.level_timer_running:
                s.level_time += dt
            ensure_music(s, "game")
            update_gameplay(s, dt)
            update_effects(s.effects, dt)

            draw_world(s, s.render_surface, cam)

            for e in s.effects:
                e.draw(s.render_surface, cam)
                
            draw_timer(s.render_surface, s)
            scaled = pygame.transform.scale(
                s.render_surface, s.screen.get_size()
            )
            s.screen.blit(scaled, (0, 0))
            pygame.display.flip()

