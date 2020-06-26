from enum import IntEnum, auto
from typing import Optional, Tuple

import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans

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


def cvtColor(o: ColorMode, n: ColorMode):
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


def color_quantization(n_clusters: int) -> Filter:
    @filter_opencv
    def f(img: np.ndarray) -> np.ndarray:
        h, w, _ = img.shape
        X = img.reshape((h * w, 3))
        k_means = MiniBatchKMeans(n_clusters=n_clusters, random_state=0)

        labels = k_means.fit_predict(X)
        values = k_means.cluster_centers_.astype('uint8')

        return values[labels].reshape((h, w, 3))

    return f
