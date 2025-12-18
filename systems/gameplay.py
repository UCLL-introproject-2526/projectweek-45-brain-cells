from settings import *
from players.merged_player import MergedPlayer
from players.merge_effect import MergeEffect

from systems.helpers import (
    distance,
    hit_spikes,
    hit_cannonballs,
    hit_goblins,
    fell_out_of_world
)
from systems.spawn_resolution import resolve_spawn_collision

from save.save_manager import save_game
from level.registry import save_levels_json


def update_gameplay(state, dt):
    # -------------------------
    # GAMEPLAY
    # -------------------------
    state.merge_cooldown = max(0.0, state.merge_cooldown - dt)

    if state.merged is None:
        solids = state.level.solids()
        state.player1.update(dt, solids, [state.player2])
        state.player2.update(dt, solids, [state.player1])

        if (
            state.merge_cooldown <= 0
            and (state.p1_input.merge_pressed() or state.p2_input.merge_pressed())
            and distance(state.player1, state.player2) <= MERGE_DISTANCE
        ):
            state.effects.append(MergeEffect(state.player1.rect.center))

            mx = (
                state.player1.rect.centerx
                + state.player2.rect.centerx
            ) // 2 - MERGED_W // 2
            my = min(state.player1.rect.top, state.player2.rect.top) - 4

            state.merged = MergedPlayer(mx, my, state.p1_input, state.p2_input)

            if hasattr(state.merged, "vel"):
                state.merged.vel.xy = (0, 0)
            if hasattr(state.merged, "on_ground"):
                state.merged.on_ground = False
            if hasattr(state.merged, "just_merged"):
                state.merged.just_merged = True

            resolve_spawn_collision(state.merged.rect, state.level.solids())
            state.merge_cooldown = MERGE_COOLDOWN_SEC

    else:
        state.merged.update(dt, state.level.solids(), state.level.blocks)

        if state.merge_cooldown <= 0 and state.merged.wants_split():
            state.effects.append(MergeEffect(state.merged.rect.center))

            solids = state.level.solids()
            split_dx = max(PLAYER_W, 28)

            state.player1.rect.midbottom = (
                state.merged.rect.centerx - split_dx,
                state.merged.rect.bottom
            )
            state.player2.rect.midbottom = (
                state.merged.rect.centerx + split_dx,
                state.merged.rect.bottom
            )

            resolve_spawn_collision(state.player1.rect, solids)
            resolve_spawn_collision(state.player2.rect, solids)

            state.player1.vel.xy = (0, 0)
            state.player2.vel.xy = (0, 0)

            state.merged = None
            state.merge_cooldown = MERGE_COOLDOWN_SEC

    active = [state.merged] if state.merged else [state.player1, state.player2]
    state.level.update(dt, active)

    # -------------------------
    # DEATH
    # -------------------------
    died = False
    if state.merged:
        if (
            hit_spikes(state.merged, state.level.spikes)
            or hit_cannonballs(state.merged, state.level.cannonballs)
            or hit_goblins(state.merged, state.level.goblins)
            or fell_out_of_world(state.merged)
        ):
            state.merged = None
            died = True
    else:
        if (
            hit_spikes(state.player1, state.level.spikes)
            or hit_spikes(state.player2, state.level.spikes)
            or hit_cannonballs(state.player1, state.level.cannonballs)
            or hit_cannonballs(state.player2, state.level.cannonballs)
            or hit_goblins(state.player1, state.level.goblins)
            or hit_goblins(state.player2, state.level.goblins)
            or fell_out_of_world(state.player1)
            or fell_out_of_world(state.player2)
        ):
            died = True

    if died:
        state.player1.rect.topleft = state.level.spawn_p1
        state.player2.rect.topleft = state.level.spawn_p2
        state.player1.vel.xy = (0, 0)
        state.player2.vel.xy = (0, 0)

        # ⏱ reset timer on death
        state.level_time = 0.0
        state.level_timer_running = True

    # -------------------------
    # WIN / TIMER / POPUP
    # -------------------------
    if state.merged and state.level.finish:
        if state.merged.rect.colliderect(state.level.finish.rect):
            state.level_timer_running = False

            new_time = round(state.level_time, 3)
            level_data = state.levels_data[state.level_index]

            best = level_data.get("best_time")
            is_new_record = best is None or new_time < best

            if is_new_record:
                level_data["best_time"] = new_time
                save_levels_json(state.levels_data)

            # unlock next level
            if state.level_index + 1 > state.unlocked_levels:
                state.unlocked_levels = state.level_index + 1
                state.save_data["unlocked_levels"] = state.unlocked_levels
                save_game(state.save_data)

            from ui.level_complete_popup import LevelCompletePopup

            state.level_complete_popup = LevelCompletePopup(
                state.font_big,
                state.font_small,
                new_time,
                level_data.get("best_time"),
                is_new_record
            )

            state.merged = None

