import pygame

from state.game_state import GameState
from systems.input_building import build_inputs
from systems.effects import update_effects
from systems.gameplay import update_gameplay
from rendering.draw import draw_world


class GameApp:
    def __init__(self):
        self.state = GameState()
        self.state.load_level(0)
        self.state.level_menu.open()

    def run(self):
        s = self.state

        while s.running:
            dt = s.clock.tick(60) / 1000.0
            s.t += dt

            # clear render surface
            s.render_surface.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    s.running = False

            keys = pygame.key.get_pressed()

            # -------------------------
            # MENU TOGGLES (EDGE TRIGGER)
            # -------------------------
            if keys[pygame.K_m] and not s.menu_key_prev:
                s.settings_menu.toggle()
                s.level_menu.visible = False
            s.menu_key_prev = keys[pygame.K_m]

            if keys[pygame.K_l] and not s.level_key_prev:
                s.level_menu.open()
                s.settings_menu.visible = False
            s.level_key_prev = keys[pygame.K_l]

            # -------------------------
            # CAMERA UPDATE
            # -------------------------
            s.camera.update(
                [s.merged.rect] if s.merged else [s.player1.rect, s.player2.rect]
            )
            cam = s.camera.offset()

            # ============================================================
            # LEVEL MENU (DRAW WORLD → SCALE → DRAW MENU → FLIP)
            # ============================================================
            if s.level_menu.visible:
                choice = s.level_menu.handle_input(
                    s.level_names, s.unlocked_levels
                )
                if choice is not None:
                    s.load_level(choice)
                    s.level_menu.close()

                # draw world to render surface
                draw_world(s, s.render_surface, cam)

                # scale world to screen
                scaled = pygame.transform.scale(
                    s.render_surface, s.screen.get_size()
                )
                s.screen.blit(scaled, (0, 0))

                # draw menu ON TOP
                s.level_menu.draw(
                    s.screen, s.level_names, s.unlocked_levels
                )

                pygame.display.flip()
                continue

            # ============================================================
            # SETTINGS MENU (DRAW WORLD → SCALE → DRAW MENU → FLIP)
            # ============================================================
            if s.settings_menu.visible:
                s.settings_menu.handle_input()

                # rebuild inputs (same as original behavior)
                s.p1_input, s.p2_input = build_inputs(
                    s.settings_menu.layouts[s.settings_menu.layout_index]
                )
                s.p1_input.reset()
                s.p2_input.reset()

                s.player1.input = s.p1_input
                s.player2.input = s.p2_input

                pygame.mixer.music.set_volume(
                    s.settings_menu.volume / 100.0
                )

                # draw world
                draw_world(s, s.render_surface, cam)

                # scale world to screen
                scaled = pygame.transform.scale(
                    s.render_surface, s.screen.get_size()
                )
                s.screen.blit(scaled, (0, 0))

                # draw settings ON TOP
                s.settings_menu.draw(s.screen)

                pygame.display.flip()
                continue

            # ============================================================
            # GAMEPLAY
            # ============================================================
            update_gameplay(s, dt)

            # -------------------------
            # EFFECTS
            # -------------------------
            update_effects(s.effects, dt)

            # -------------------------
            # DRAW (NORMAL GAMEPLAY)
            # -------------------------
            draw_world(s, s.render_surface, cam)

            for e in s.effects:
                e.draw(s.render_surface, cam)

            scaled = pygame.transform.scale(
                s.render_surface, s.screen.get_size()
            )
            s.screen.blit(scaled, (0, 0))
            pygame.display.flip()
