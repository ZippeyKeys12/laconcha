from math import radians
from typing import Tuple, Union

from skimage.transform import AffineTransform
from skimage.transform import rotate as sk_rotate
from skimage.transform import warp

import numpy as np

from ..decorators import gen_meta
from ..image import Filter
from ..ranges import Range
from .decorators import filter_numpy


@gen_meta((Range(-1024, 1024, default=0), Range(-1024, 1024, default=0)))
def translate(vector: Tuple[float, float]) -> Filter:
    return transform(AffineTransform(translation=vector))


@gen_meta(Range(.1, 10, default=1), Range(.1, 10, default=1))
def scale(multiplier: Union[float, Tuple[float, float]]) -> Filter:
    return transform(AffineTransform(scale=1 / np.array(multiplier)))


@gen_meta(Range(0.0, 360))
def rotate(angle: float) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return sk_rotate(img, angle)

    return f


@gen_meta(Range(0.0, 90))
def shear(angle: float) -> Filter:
    return transform(AffineTransform(shear=radians(angle)))


def transform(t: AffineTransform) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return warp(img, t)

    return f
