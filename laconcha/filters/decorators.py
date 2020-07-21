from __future__ import annotations

from typing import Callable
from functools import wraps
from PIL.Image import Image as PILImage

import numpy as np

from ..image import Filter, Image, ImageMode

OpenCVFilter = Callable[[np.ndarray], np.ndarray]


def filter_opencv(f: OpenCVFilter) -> Filter:
    @wraps(f)
    def new_f(img: Image) -> Image:
        return Image.from_opencv(f(img.as_opencv()))

    return new_f


PILFilter = Callable[[PILImage], PILImage]


def filter_pil(f: PILFilter) -> Filter:
    @wraps(f)
    def new_f(img: Image) -> Image:
        return Image.from_pil(f(img.as_pil()))

    return new_f


ScikitFilter = Callable[[np.ndarray], np.ndarray]


def filter_scikit(f: ScikitFilter) -> Filter:
    @wraps(f)
    def new_f(img: Image) -> Image:
        return Image.from_scikit(f(img.as_scikit()))

    return new_f


NumPyFilter = Callable[[np.ndarray], np.ndarray]


def filter_numpy(f: NumPyFilter) -> Filter:
    @wraps(f)
    def new_f(img: Image) -> Image:
        if img.mode == ImageMode.PIL:
            i = img.as_opencv()
        else:
            i = img.img

        res = f(i)

        if img.mode == ImageMode.OPENCV:
            return Image.from_opencv(res)

        if img.mode == ImageMode.SCIKIT:
            return Image.from_scikit(res)

        raise RuntimeError('what')

    return new_f
