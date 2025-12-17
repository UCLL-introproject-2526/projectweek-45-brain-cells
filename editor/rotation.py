# editor/rotation.py

ROTATION_ORDER = [">", "v", "<", "^"]


def rotate_char(ch):
    if ch not in ROTATION_ORDER:
        return ch

    i = ROTATION_ORDER.index(ch)
    return ROTATION_ORDER[(i + 1) % len(ROTATION_ORDER)]
