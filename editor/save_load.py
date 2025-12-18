# editor/save_load.py
from level.registry import load_all_levels, save_levels_json


def save_level(editor_state, level_index=None):
    """
    Save the current editor state into levels.json.

    - If level_index is None → create new level
    - If level_index is provided → overwrite existing level
    """
    levels_data = load_all_levels()

    level_entry = {
        "name": editor_state.level_name,
        "map_data": ["".join(row) for row in editor_state.map_data],
        "background": editor_state.background_path,
    }

    # preserve best_time if overwriting
    if level_index is not None:
        old = levels_data[level_index]
        if "best_time" in old:
            level_entry["best_time"] = old["best_time"]
        levels_data[level_index] = level_entry
    else:
        level_entry["best_time"] = None
        levels_data.append(level_entry)

    save_levels_json(levels_data)
    print("[Editor] Level saved to levels.json")


def save_preview_level(editor_state):
    """
    Optional: overwrite a special preview slot.
    This assumes your game loads index 0 or a known index for preview.
    """
    levels_data = load_all_levels()

    preview_entry = {
        "name": f"[EDITOR PREVIEW] {editor_state.level_name}",
        "map_data": ["".join(row) for row in editor_state.map_data],
        "background": editor_state.background_path,
        "best_time": None,
    }

    # put preview at index 0 (or change if you prefer)
    if levels_data:
        levels_data[0] = preview_entry
    else:
        levels_data.append(preview_entry)

    save_levels_json(levels_data)
    print("[Editor] Preview level saved to levels.json")
