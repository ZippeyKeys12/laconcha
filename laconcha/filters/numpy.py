from typing import Optional, Tuple

import cv2
from skimage.transform import integral_image
from skimage.transform import swirl as sk_swirl
from skimage.util import img_as_float
from sklearn.cluster import MiniBatchKMeans

import numpy as np

from ..curves import Curve
from ..image import Filter
from .decorators import filter_numpy


def mean_filter(kernel_size: Tuple[int, int]) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.blur(img, kernel_size)

    return f


def gaussian_blur(kernel_size: Tuple[int, int], std_dev: Optional[float] = None) -> Filter:
    std_dev = std_dev or 0

    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.GaussianBlur(img, kernel_size, std_dev)

    return f


def median_filter(kernel_size: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.medianBlur(img, kernel_size)

    return f


def bilateral_filter(diameter: int, std_dev_color: float, std_dev_space: float) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.bilateralFilter(img, diameter, std_dev_color, std_dev_space)

    return f


def color_quantization(n_clusters: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        h, w, _ = img.shape
        X = img.reshape((h * w, 3))
        k_means = MiniBatchKMeans(n_clusters=n_clusters, random_state=0)

        labels = k_means.fit_predict(X)
        values = k_means.cluster_centers_.astype('uint8')

        return values[labels].reshape((h, w, 3))

    return f


def swirl(center: Optional[Tuple[float, float]] = None, strength: float = 1, radius: float = 100) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return sk_swirl(img, center, strength, radius)

    return f


@filter_numpy
def integral(img: np.ndarray) -> np.ndarray:
    return integral_image(img)


def curve(c: Curve) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return np.reshape([c(x) for x in img_as_float(img.flatten())], img.shape)

    return f


def shuffle(seed: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        h, w, _ = img.shape
        gen = np.random.default_rng(seed)

        img = img.copy().reshape(h * w, 3)
        gen.shuffle(img)
        return img.reshape(h, w, 3)

    return f
