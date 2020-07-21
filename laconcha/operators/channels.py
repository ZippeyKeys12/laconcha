import numpy as np

from ..image import ColorChannel, Operator
from .decorators import operator_opencv


def set_channel(ch: ColorChannel) -> Operator:
    index = ch.value

    @operator_opencv
    def f(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        res = a.copy()
        res[:, :, index] = b[:, :, index]
        return res

    return f
