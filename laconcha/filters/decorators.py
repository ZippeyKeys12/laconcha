from __future__ import annotations

from typing import Callable

import numpy as np
from PIL.Image import Image as PILImage
from skimage.util import img_as_ubyte

from ..image import Filter, Image, ImageMode

OpenCVFilter = Callable[[np.ndarray], np.ndarray]


def filter_opencv(f: OpenCVFilter) -> Filter:
    def new_f(img: Image) -> Image:
        return Image.from_opencv(f(img.as_opencv()))

    return new_f


PILFilter = Callable[[PILImage], PILImage]


def filter_pil(f: PILFilter) -> Filter:
    def new_f(img: Image) -> Image:
        return Image.from_pil(f(img.as_pil()))

    return new_f


ScikitFilter = Callable[[np.ndarray], np.ndarray]


def filter_scikit(f: ScikitFilter) -> Filter:
    def new_f(img: Image) -> Image:
        return Image.from_scikit(img_as_ubyte(f(img.as_scikit())))

    return new_f


NumPyFilter = Callable[[np.ndarray], np.ndarray]


def filter_numpy(f: NumPyFilter) -> Filter:
    def new_f(img: Image) -> Image:
        mode = img.mode

        if mode == ImageMode.PIL:
            i = img.as_opencv()
            mode = ImageMode.OPENCV
        else:
            i = img.img

        res = f(i)

        if mode == ImageMode.OPENCV:
            return Image.from_opencv(res)

        if mode == ImageMode.SCIKIT:
            return Image.from_scikit(res)

        raise RuntimeError('what')

    return new_f
