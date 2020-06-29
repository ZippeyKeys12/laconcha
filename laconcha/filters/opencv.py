from enum import IntEnum, auto
from typing import Optional, Tuple

import cv2
import numpy as np

from .decorators import Filter, filter_opencv


def mean_filter(kernel_size: Tuple[int, int]) -> Filter:
    @filter_opencv
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.blur(img, kernel_size)

    return f


def gaussian_blur(kernel_size: Tuple[int, int], std_dev: Optional[float] = None) -> Filter:
    std_dev = std_dev or 0

    @filter_opencv
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.GaussianBlur(img, kernel_size, std_dev)

    return f


def median_filter(kernel_size: int) -> Filter:
    @filter_opencv
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.medianBlur(img, kernel_size)

    return f


def bilateral_filter(diameter: int, std_dev_color: float, std_dev_space: float) -> Filter:
    @filter_opencv
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.bilateralFilter(img, diameter, std_dev_color, std_dev_space)

    return f


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
    conv = _color_convs[o][n]

    if isinstance(conv, (list, tuple)):
        @filter_opencv
        def f(img: np.ndarray) -> np.ndarray:
            for c in conv:
                img = cv2.cvtColor(img, c)
            return img

    else:
        @filter_opencv
        def f(img: np.ndarray) -> np.ndarray:
            return cv2.cvtColor(img, conv)

    return f


class ColorChannel(IntEnum):
    B = 0
    G = 1
    R = 2


def channel(ch: ColorChannel) -> Filter:
    index = ch.value

    @filter_opencv
    def f(img: np.ndarray) -> np.ndarray:
        res = np.empty_like(img)
        res[:, :, 0] = img[:, :, index]
        res[:, :, 1] = img[:, :, index]
        res[:, :, 2] = img[:, :, index]
        return res

    return f





