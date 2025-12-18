ROTATION_MAP = {
    ">": "v",
    "v": "<",
    "<": "^",
    "^": ">"
}


def rotate_char(ch):
    """
    Rotate a rotatable ASCII character.
    If character is not rotatable, return it unchanged.
    """
    return ROTATION_MAP.get(ch, ch)
