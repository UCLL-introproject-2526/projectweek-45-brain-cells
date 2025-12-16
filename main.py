import pygame
from settings import *

from utils.input import PlayerInput
from players.player import Player
from players.merged_player import MergedPlayer
from players.merge_effect import MergeEffect

from core.camera import Camera
from ui.settings_menu import SettingsMenu
from ui.level_select_menu import LevelSelectMenu

from level.registry import discover_levels
from save.save_manager import load_save, save_game


# -----------------------------
# INPUT BUILDING
# -----------------------------
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


def distance(a, b):
    dx = a.rect.centerx - b.rect.centerx
    dy = a.rect.centery - b.rect.centery
    return (dx * dx + dy * dy) ** 0.5


def hit_spikes(actor, spikes):
    return any(actor.rect.colliderect(s.rect) for s in spikes)


def fell_out_of_world(actor):
    return actor.rect.top > KILL_Y


# -----------------------------
# INIT
# -----------------------------
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Split / Merge Dungeon")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

camera = Camera()
settings_menu = SettingsMenu(font)
level_menu = LevelSelectMenu(font)
effects = []

# SAVE DATA
save_data = load_save()
unlocked_levels = save_data.get("unlocked_levels", 1)

# LEVELS
level_classes = discover_levels("level")
level_names = [getattr(c, "name", c.__name__) for c in level_classes]

# INPUTS
p1_input, p2_input = build_inputs("QWERTY")

player1 = Player(120, 100, p1_input, (80, 160, 255))
player2 = Player(200, 100, p2_input, (255, 170, 80))

merged = None
merge_cooldown = 0.0
menu_key_prev = False
level_key_prev = False
t = 0.0
running = True

level = None


def draw_actors(screen, cam):
    if merged:
        merged.draw(screen, cam)
    else:
        player1.draw(screen, cam)
        player2.draw(screen, cam)


def load_level(idx):
    global level, merged
    merged = None
    level = level_classes[idx]()

    player1.rect.topleft = level.spawn_p1
    player2.rect.topleft = level.spawn_p2
    player1.vel.xy = (0, 0)
    player2.vel.xy = (0, 0)

    effects.clear()


load_level(0)
level_menu.open()

# -----------------------------
# MAIN LOOP
# -----------------------------
while running:
    dt = clock.tick(FPS) / 1000.0
    t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Toggle settings
    if keys[pygame.K_m] and not menu_key_prev:
        settings_menu.toggle()
        level_menu.visible = False
    menu_key_prev = keys[pygame.K_m]

    # Toggle level select
    if keys[pygame.K_l] and not level_key_prev:
        level_menu.open()
        settings_menu.visible = False
    level_key_prev = keys[pygame.K_l]

    camera.update([merged.rect] if merged else [player1.rect, player2.rect])
    cam = camera.offset()

    # -------------------------
    # LEVEL MENU
    # -------------------------
    if level_menu.visible:
        choice = level_menu.handle_input(level_names, unlocked_levels)
        if choice is not None:
            load_level(choice)
            level_menu.close()

        level.draw_background(screen, cam, t)
        level.draw(screen, cam)
        draw_actors(screen, cam)

        level_menu.draw(screen, level_names, unlocked_levels)
        pygame.display.flip()
        continue

    # -------------------------
    # SETTINGS MENU
    # -------------------------
    if settings_menu.visible:
        settings_menu.handle_input()

        p1_input, p2_input = build_inputs(
            settings_menu.layouts[settings_menu.layout_index]
        )
        p1_input.reset()
        p2_input.reset()

        player1.input = p1_input
        player2.input = p2_input

        pygame.mixer.music.set_volume(settings_menu.volume / 100.0)

        level.draw_background(screen, cam, t)
        level.draw(screen, cam)
        draw_actors(screen, cam)

        settings_menu.draw(screen)
        pygame.display.flip()
        continue

    # -------------------------
    # GAMEPLAY
    # -------------------------
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

    # -------------------------
    # DEATH
    # -------------------------
    died = False
    if merged:
        if hit_spikes(merged, level.spikes) or fell_out_of_world(merged):
            merged = None
            died = True
    else:
        if (hit_spikes(player1, level.spikes) or hit_spikes(player2, level.spikes)
                or fell_out_of_world(player1) or fell_out_of_world(player2)):
            died = True

    if died:
        player1.rect.topleft = level.respawn_p1
        player2.rect.topleft = level.respawn_p2
        player1.vel.xy = (0, 0)
        player2.vel.xy = (0, 0)

    # -------------------------
    # WIN / UNLOCK (MERGED ONLY)
    # -------------------------
    if merged and level.goal:
        if merged.rect.colliderect(level.goal.rect):
            idx = level_classes.index(type(level))
            if idx + 1 > unlocked_levels:
                unlocked_levels = idx + 1
                save_data["unlocked_levels"] = unlocked_levels
                save_game(save_data)

            merged = None
            level_menu.open()

    # -------------------------
    # EFFECTS
    # -------------------------
    for e in effects[:]:
        e.update(dt)
        if e.done:
            effects.remove(e)

    # -------------------------
    # DRAW
    # -------------------------
    level.draw_background(screen, cam, t)
    level.draw(screen, cam)
    draw_actors(screen, cam)

    for e in effects:
        e.draw(screen, cam)

    pygame.display.flip()

pygame.quit()
