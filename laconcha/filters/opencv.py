
from enum import IntEnum

import numpy as np

from .decorators import Filter, filter_opencv


class ColorChannel(IntEnum):
    B = 0
    G = 1
    R = 2


def channel(ch: ColorChannel) -> Filter:
    index = ch.value

    @filter_opencv
    def f(img: np.ndarray) -> np.ndarray:
        res = np.empty_like(img)
        res[:, :, 0] = img[:, :, index]
        res[:, :, 1] = img[:, :, index]
        res[:, :, 2] = img[:, :, index]
        return res

    return f





