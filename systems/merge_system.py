from players.merged_player import MergedPlayer
from players.merge_effect import MergeEffect
from settings import MERGE_DISTANCE, MERGE_COOLDOWN_SEC, MERGED_W
from utils.math_utils import distance
from systems.spawn_system import resolve_spawn_collision

def try_merge(state):
    p1, p2 = state.player1, state.player2

    if state.merge_cooldown > 0:
        return

    if distance(p1, p2) > MERGE_DISTANCE:
        return

    state.effects.append(MergeEffect(p1.rect.center))

    mx = (p1.rect.centerx + p2.rect.centerx) // 2 - MERGED_W // 2
    my = min(p1.rect.top, p2.rect.top) - 4

    state.merged = MergedPlayer(mx, my, state.p1_input, state.p2_input)
    state.merge_cooldown = MERGE_COOLDOWN_SEC

    resolve_spawn_collision(state.merged.rect, state.level.solids())
