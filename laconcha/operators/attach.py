import numpy as np

from ..image import Operator
from .decorators import operator_numpy


def vattach() -> Operator:
    @operator_numpy
    def f(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.append(a, b, axis=0)

    return f


def hattach() -> Operator:
    @operator_numpy
    def f(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.append(a, b, axis=1)

    return f
