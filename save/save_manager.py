import json
import os

SAVE_FILE = "savegame.json"

DEFAULT_DATA = {
    "unlocked_levels": 1
}

def load_save():
    if not os.path.exists(SAVE_FILE):
        return DEFAULT_DATA.copy()

    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA.copy()

def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)
