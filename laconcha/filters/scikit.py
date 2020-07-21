from enum import IntEnum, auto

import cv2

import numpy as np

from ..image import Filter
from .base import identity
from .decorators import filter_scikit


class ColorMode(IntEnum):
    RGB = auto()
    BGR = auto()
    HSV = auto()
    LAB = auto()


_color_convs = {
    ColorMode.RGB: {
        ColorMode.BGR: cv2.COLOR_RGB2BGR,
        ColorMode.HSV: cv2.COLOR_RGB2HSV,
        ColorMode.LAB: cv2.COLOR_RGB2LAB
    },
    ColorMode.BGR: {
        ColorMode.RGB: cv2.COLOR_BGR2RGB,
        ColorMode.HSV: cv2.COLOR_BGR2HSV,
        ColorMode.LAB: cv2.COLOR_BGR2LAB
    },
    ColorMode.HSV: {
        ColorMode.RGB: cv2.COLOR_HSV2RGB,
        ColorMode.BGR: cv2.COLOR_HSV2BGR,
        ColorMode.LAB: [cv2.COLOR_HSV2BGR, cv2.COLOR_BGR2LAB]
    },
    ColorMode.LAB: {
        ColorMode.RGB: cv2.COLOR_LAB2RGB,
        ColorMode.BGR: cv2.COLOR_LAB2BGR,
        ColorMode.HSV: [cv2.COLOR_LAB2BGR, cv2.COLOR_BGR2HSV]
    }
}


def convert_color(o: ColorMode, n: ColorMode) -> Filter:
    if o == n:
        return identity()

    conv = _color_convs[o][n]

    if isinstance(conv, (list, tuple)):
        @filter_scikit
        def f(img: np.ndarray) -> np.ndarray:
            for c in conv:
                img = cv2.cvtColor(img, c)
            return img

    else:
        @filter_scikit
        def f(img: np.ndarray) -> np.ndarray:
            return cv2.cvtColor(img, conv)

    return f
