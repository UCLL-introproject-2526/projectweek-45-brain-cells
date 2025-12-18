import importlib
import inspect
import os




def load_level_into_editor(level_module_name, EditorStateCls):
    """
    Loads an existing level class WITHOUT instantiating gameplay logic.
    Extracts ASCII map data safely for the editor.
    """

    # import module (e.g. level.levels.level0)
    module = importlib.import_module(level_module_name)

    level_class = None

    def ensure_mutable(self):
        self.map_data = [
            list(row) if isinstance(row, str) else row
            for row in self.map_data
        ]

    # find LevelX class inside module
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module.__name__:
            level_class = obj
            break

    if level_class is None:
        raise RuntimeError(f"No level class found in {level_module_name}")

    # ---- SAFE DATA EXTRACTION (NO __init__) ----
    map_data = getattr(level_class, "map_data", None)
    name = getattr(level_class, "name", "Unnamed Level")

    if not map_data:
        raise ValueError("Level has no map_data")

    h = len(map_data)
    w = len(map_data[0])

    # create editor state
    state = EditorStateCls(grid_w=w, grid_h=h)
    state.level_name = name

    # copy map data safely
    state.map_data = [list(row) for row in map_data]

    # background (optional)
    if hasattr(level_class, "background"):
        state.background_path = level_class.background

    return state
