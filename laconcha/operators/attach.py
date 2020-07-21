import numpy as np

from .decorators import operator_numpy


@operator_numpy
def vattach(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.append(a, b, axis=0)


@operator_numpy
def hattach(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.append(a, b, axis=1)
