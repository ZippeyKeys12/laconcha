from __future__ import annotations

from typing import Callable

import numpy as np
from PIL.Image import Image as PILImage

from ..image import Image, Operator

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
