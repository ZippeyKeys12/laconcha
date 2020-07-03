from typing import Tuple

from PIL import Image as PILImage
from PIL import ImageOps

import numpy as np

from ..image import Filter
from .decorators import filter_numpy, filter_pil


def crop(size: Tuple[int, int]) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        h, w, _ = img.shape
        cy, cx = h // 2, w // 2
        qy, qx = size[0] // 2, size[1] // 2
        return img[cy - qy: cy + qy, cx - qx:cx + qx, :]

    return f


def fit(size: Tuple[int, int]) -> Filter:
    size = size[::-1]

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return ImageOps.fit(img, size)

    return f


def top(pixels: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return img[:pixels, :, :]

    return f


def bottom(pixels: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return img[img.shape[0] - pixels:, :, :]

    return f


def left(pixels: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return img[:, :pixels, :]

    return f


def right(pixels: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return img[:, img.shape[1] - pixels:, :]

    return f
