from typing import Optional, Tuple

import cv2
from skimage.transform import integral_image
from skimage.transform import swirl as sk_swirl
from skimage.util import img_as_float
from sklearn.cluster import MiniBatchKMeans

import numpy as np
from laconcha.curves import (circular, cosine, cubic, exponential, inverse,
                             logarithm, quadratic, sine, smooth_step,
                             smoother_step, smoothest_step, square_root)

from ..curves import Curve
from ..decorators import gen_meta
from ..image import Filter
from ..ranges import Range
from ..seed import Seed
from .decorators import filter_numpy


@gen_meta((Range(1, 8, default=5), Range(1, 8, default=5)))
def mean_filter(kernel_size: Tuple[int, int]) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.blur(img, kernel_size)

    return f


@gen_meta((Range(1, 8, 2, 5), Range(1, 8, 2, 5)), Range(0.0, 10))
def gaussian_blur(kernel_size: Tuple[int, int], std_dev: Optional[float] = None) -> Filter:
    std_dev = std_dev or 0

    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.GaussianBlur(img, kernel_size, std_dev)

    return f


@gen_meta(Range(1, 16, 2, 9))
def median_filter(kernel_size: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.medianBlur(img, kernel_size)

    return f


@gen_meta(Range(1, 16, default=9), Range(0, 101, default=75), Range(0, 101, default=75))
def bilateral_filter(diameter: int, std_dev_color: float, std_dev_space: float) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return cv2.bilateralFilter(img, diameter, std_dev_color, std_dev_space)

    return f


@gen_meta(Range(1, 129, default=16))
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


@gen_meta(Range(0.0, 100), Range(1.0, 1024))
def swirl(strength: float, radius: float) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return sk_swirl(img, strength=strength, radius=radius)

    return f


@gen_meta()
@filter_numpy
def integral(img: np.ndarray) -> np.ndarray:
    return integral_image(img)


@gen_meta([
    circular,
    cosine,
    cubic,
    exponential,
    inverse,
    logarithm,
    sine,
    smooth_step,
    smoother_step,
    smoothest_step,
    square_root,
    quadratic
])
def curve(c: Curve) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return np.reshape([c(x) for x in img_as_float(img.flatten())], img.shape)

    return f


@gen_meta(Seed())
def shuffle(seed: int) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        h, w, _ = img.shape
        gen = np.random.default_rng(seed)

        img = img.copy().reshape(h * w, 3)
        gen.shuffle(img)
        return img.reshape(h, w, 3)

    return f
