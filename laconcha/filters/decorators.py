from __future__ import annotations

from typing import Callable

import numpy as np
from PIL.Image import Image as PILImage
from skimage.util import img_as_ubyte

from ..image import Filter, Image

OpenCVFilter = Callable[[np.ndarray], np.ndarray]


def filter_opencv(f: OpenCVFilter) -> Filter:
    def new_f(img: Image):
        return Image.from_opencv(f(img.as_opencv()))

    return new_f


PILFilter = Callable[[PILImage], PILImage]


def filter_pil(f: PILFilter) -> Filter:
    def new_f(img: Image):
        return Image.from_pil(f(img.as_pil()))

    return new_f


ScikitFilter = Callable[[np.ndarray], np.ndarray]


def filter_scikit(f: ScikitFilter) -> Filter:
    def new_f(img: Image):
        return Image.from_scikit(img_as_ubyte(f(img.as_scikit())))

    return new_f
