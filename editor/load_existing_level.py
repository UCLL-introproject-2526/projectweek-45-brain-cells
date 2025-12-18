# editor/load_existing_level.py

from editor.editor_state import EditorState
from level.registry import load_all_levels


def load_level_into_editor(level_index, EditorStateClass):
    """
    Load a level from levels.json into the editor.
    `level_index` is an int.
    """

    levels_data = load_all_levels()

    if level_index < 0 or level_index >= len(levels_data):
        raise IndexError("Invalid level index")

    level_data = levels_data[level_index]

    map_rows = [list(row) for row in level_data["map_data"]]
    height = len(map_rows)
    width = len(map_rows[0])

    # Create editor state
    state = EditorStateClass(grid_w=width, grid_h=height)

    # Restore editor data
    state.map_data = map_rows
    state.level_name = level_data.get("name", "Unnamed Level")
    state.background_path = level_data.get("background")

    return state
