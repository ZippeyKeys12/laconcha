from typing import Tuple

from PIL import Image as PILImage
from PIL import ImageOps

import numpy as np

from ..decorators import gen_meta
from ..image import Filter
from ..ranges import Range
from .decorators import filter_numpy, filter_pil


@gen_meta(Range(0, 1024, 2), Range(0, 1024, 2))
def crop(size: Tuple[int, int]) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        h, w, _ = img.shape
        cy, cx = h // 2, w // 2
        qy, qx = size[0] // 2, size[1] // 2
        return img[cy - qy: cy + qy, cx - qx:cx + qx, :]

    return f


@gen_meta(Range(0, 1024, 2), Range(0, 1024, 2))
def fit(size: Tuple[int, int]) -> Filter:
    size = size[::-1]

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return ImageOps.fit(img, size)

    return f


@gen_meta(Range(0, 1024, 2))
def top(pixels: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return img[:pixels, :, :]

    return f


@gen_meta(Range(0, 1024, 2))
def bottom(pixels: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return img[img.shape[0] - pixels:, :, :]

    return f


@gen_meta(Range(0, 1024, 2))
def left(pixels: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return img[:, :pixels, :]

    return f


@gen_meta(Range(0, 1024, 2))
def right(pixels: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return img[:, img.shape[1] - pixels:, :]

    return f
