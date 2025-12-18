import json
from level.json_level import JsonLevel

LEVELS_FILE = "levels.json"


def load_all_levels():
    with open(LEVELS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["levels"]


def get_level_names(levels_data):
    return [lvl["name"] for lvl in levels_data]


def load_level(index, levels_data):
    return JsonLevel(levels_data[index])


def save_levels_json(levels_data):
    with open(LEVELS_FILE, "w", encoding="utf-8") as f:
        json.dump({"levels": levels_data}, f, indent=2)