import numpy as np

from ..image import ColorChannel
from .decorators import Filter, filter_opencv


def get_channel(ch: ColorChannel) -> Filter:
    index = ch.value

    @filter_opencv
    def f(img: np.ndarray) -> np.ndarray:
        res = np.empty_like(img)
        res[:, :, 0] = img[:, :, index]
        res[:, :, 1] = img[:, :, index]
        res[:, :, 2] = img[:, :, index]
        return res

    return f
