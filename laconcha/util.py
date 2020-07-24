from typing import Tuple

import numpy as np

RGBColor = Tuple[int, int, int]


def safe_divide(a, b):
    return np.divide(a, np.maximum(b, .0001))


def format_name(x: str) -> str:
    return ' '.join(i.capitalize() for i in x.split('_'))


def hex_to_rgb(hexcode: str) -> Tuple[int, int, int]:
    hexcode = hexcode[1:]

    return (int(hexcode[:2], 16), int(hexcode[2:4], 16), int(hexcode[4:], 16))
