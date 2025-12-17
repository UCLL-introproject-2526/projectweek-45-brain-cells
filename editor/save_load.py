# editor/save_load.py
import os


def next_level_index(levels_dir="level/levels"):
    os.makedirs(levels_dir, exist_ok=True)

    max_idx = 0
    for name in os.listdir(levels_dir):
        if name.startswith("level") and name.endswith(".py"):
            num = name[5:-3]
            if num.isdigit():
                max_idx = max(max_idx, int(num))

    return max_idx + 1


def save_level(state):
    idx = next_level_index()
    class_name = f"Level{idx}"
    path = os.path.join("level", "levels", f"level{idx}.py")

    map_data = ["".join(row) for row in state.map_data]

    with open(path, "w", encoding="utf-8") as f:
        f.write(
f'''from level.ascii_level import AsciiLevel


class {class_name}(AsciiLevel):
    name = "{state.level_name}"

    map_data = [
'''
        )

        for row in map_data:
            f.write(f'        "{row}",\n')

        f.write(
'''    ]

    def __init__(self):
        super().__init__()
'''
        )

        if state.background_path:
            bg = state.background_path.replace("\\", "/")
            f.write(f'        self.load_background("{bg}")\n')

    print(f"[Editor] Saved {path}")


def save_preview_level(state):
    path = os.path.join("level", "levels", "levelpreview.py")

    map_data = ["".join(row) for row in state.map_data]

    with open(path, "w", encoding="utf-8") as f:
        f.write(
f'''from level.ascii_level import AsciiLevel


class EditorPreviewLevel(AsciiLevel):
    name = "[EDITOR PREVIEW] {state.level_name}"

    map_data = [
'''
        )

        for row in map_data:
            f.write(f'        "{row}",\n')

        f.write(
'''    ]

    def __init__(self):
        super().__init__()
'''
        )

        if state.background_path:
            bg = state.background_path.replace("\\", "/")
            f.write(f'        self.load_background("{bg}")\n')
