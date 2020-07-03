from __future__ import annotations
from typing import Tuple

from typing import Callable

import numpy as np
from PIL.Image import Image as PILImage

from ..image import Image, ImageMode, Operator

OpenCVOperator = Callable[[np.ndarray, np.ndarray], np.ndarray]


def operator_opencv(f: OpenCVOperator) -> Operator:
    def new_f(a: Image, b: Image):
        return Image.from_opencv(f(a.as_opencv(), b.as_opencv()))

    return new_f


PILOperator = Callable[[PILImage, PILImage], PILImage]


def operator_pil(f: PILOperator) -> Operator:
    def new_f(a: Image, b: Image):
        return Image.from_pil(f(a.as_pil(), b.as_pil()))

    return new_f


ScikitOperator = Callable[[np.ndarray, np.ndarray], np.ndarray]


def operator_scikit(f: ScikitOperator) -> Operator:
    def new_f(a: Image, b: Image):
        return Image.from_scikit(f(a.as_scikit(), b.as_scikit()))

    return new_f


NumPyOperator = Callable[[np.ndarray, np.ndarray], np.ndarray]


def _numpyify(a: Image, b: Image):
    if a.mode == b.mode:
        if a.mode == ImageMode.PIL:
            a.as_opencv()
            b.as_opencv()

        return

    imgs = [a, b]

    if a.mode == ImageMode.PIL:
        bad = 0
        good = 1
    else:
        bad = 1
        good = 0

    if imgs[good].mode == ImageMode.OPENCV:
        imgs[bad].as_opencv()
    elif imgs[bad].mode == ImageMode.SCIKIT:
        imgs[bad].as_scikit()

    return a, b


def operator_numpy(f: NumPyOperator) -> Operator:
    def new_f(a: Image, b: Image) -> Image:
        _numpyify(a, b)

        res = f(a.img, b.img)

        if a.mode == ImageMode.OPENCV:
            return Image.from_opencv(res)

        if a.mode == ImageMode.SCIKIT:
            return Image.from_scikit(res)

        raise RuntimeError('what')

    return new_f
