import numpy as np
from skimage.transform import integral_image
from skimage.transform import swirl as sk_swirl

from ..image import Filter
from .decorators import filter_scikit


def swirl(strength: float = 1, radius: float = 100, rotation: float = 0) -> Filter:
    @filter_scikit
    def f(img: np.ndarray) -> np.ndarray:
        return sk_swirl(img, strength=strength, radius=radius, rotation=rotation)

    return f


def integral() -> Filter:
    @filter_scikit
    def f(img: np.ndarray) -> np.ndarray:
        return integral_image(img)

    return f
