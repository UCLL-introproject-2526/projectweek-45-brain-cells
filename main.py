import pygame
from settings import *
from utils.input import PlayerInput
from players.player import Player
from players.merged_player import MergedPlayer
from players.merge_effect import MergeEffect
from level.level import Level
from core.camera import Camera
from ui.settings_menu import SettingsMenu


def build_inputs(layout):
    if layout == "QWERTY":
        p1 = PlayerInput(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_e)
    else:  # AZERTY
        p1 = PlayerInput(pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_e)

    p2 = PlayerInput(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_RSHIFT)
    return p1, p2


def distance(a, b):
    dx = a.rect.centerx - b.rect.centerx
    dy = a.rect.centery - b.rect.centery
    return (dx * dx + dy * dy) ** 0.5


def hit_spikes(actor, spikes):
    return any(actor.rect.colliderect(s.rect) for s in spikes)


def fell_out_of_world(actor):
    return actor.rect.top > KILL_Y


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Split / Merge Dungeon")

font = pygame.font.SysFont(None, 36)

settings_menu = SettingsMenu(font)

level = Level()
camera = Camera()
effects = []

p1_input, p2_input = build_inputs("QWERTY")

player1 = Player(120, 100, p1_input, (80, 160, 255))
player2 = Player(200, 100, p2_input, (255, 170, 80))

merged = None
merge_cooldown = 0.0
t = 0.0
running = True

RESPAWN_P1 = (120, 100)
RESPAWN_P2 = (200, 100)

menu_key_prev = False

while running:
    dt = clock.tick(FPS) / 1000.0
    t += dt

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Toggle menu
    if keys[pygame.K_m] and not menu_key_prev:
        settings_menu.toggle()
    menu_key_prev = keys[pygame.K_m]

    if settings_menu.visible:
        settings_menu.handle_input()

        # Apply layout live
        p1_input, p2_input = build_inputs(settings_menu.layouts[settings_menu.layout_index])
        player1.input = p1_input
        player2.input = p2_input

        pygame.mixer.music.set_volume(settings_menu.volume / 100.0)

    else:
        merge_cooldown = max(0.0, merge_cooldown - dt)

        if merged is None:
            solids = level.solids()
            player1.update(dt, solids, [player2])
            player2.update(dt, solids, [player1])

            if merge_cooldown <= 0 and (p1_input.merge_pressed() or p2_input.merge_pressed()):
                if distance(player1, player2) <= MERGE_DISTANCE:
                    effects.append(MergeEffect(player1.rect.center))
                    mx = (player1.rect.centerx + player2.rect.centerx) // 2 - MERGED_W // 2
                    my = min(player1.rect.top, player2.rect.top) - 20
                    merged = MergedPlayer(mx, my, p1_input, p2_input)
                    merge_cooldown = MERGE_COOLDOWN_SEC
        else:
            merged.update(dt, level.solids(), level.blocks)

            if merge_cooldown <= 0 and merged.wants_split():
                effects.append(MergeEffect(merged.rect.center))
                player1.rect.midbottom = (merged.rect.centerx - 24, merged.rect.bottom)
                player2.rect.midbottom = (merged.rect.centerx + 24, merged.rect.bottom)
                merged = None
                merge_cooldown = MERGE_COOLDOWN_SEC

        active = [merged] if merged else [player1, player2]
        level.update(dt, active)

        died = False
        if merged:
            if hit_spikes(merged, level.spikes) or fell_out_of_world(merged):
                merged = None
                died = True
        else:
            if (
                hit_spikes(player1, level.spikes)
                or hit_spikes(player2, level.spikes)
                or fell_out_of_world(player1)
                or fell_out_of_world(player2)
            ):
                died = True

        if died:
            player1.rect.topleft = RESPAWN_P1
            player2.rect.topleft = RESPAWN_P2
            player1.vel.xy = (0, 0)
            player2.vel.xy = (0, 0)

    for e in effects[:]:
        e.update(dt)
        if e.done:
            effects.remove(e)

    camera.update([merged.rect] if merged else [player1.rect, player2.rect])
    cam = camera.offset()

    level.draw_background(screen, cam, t)
    level.draw(screen, cam)

    if merged:
        merged.draw(screen, cam)
    else:
        player1.draw(screen, cam)
        player2.draw(screen, cam)

    for e in effects:
        e.draw(screen, cam)

    if settings_menu.visible:
        settings_menu.draw(screen)

    pygame.display.flip()

pygame.quit()
