from math import radians
from typing import Tuple, Union

from skimage.transform import AffineTransform
from skimage.transform import rotate as sk_rotate
from skimage.transform import warp

import numpy as np

from ..image import Filter
from .decorators import filter_numpy


def translate(vector: Tuple[float, float]) -> Filter:
    return transform(AffineTransform(translation=vector))


def scale(multiplier: Union[float, Tuple[float, float]]) -> Filter:
    return transform(AffineTransform(scale=1 / np.array(multiplier)))


def rotate(angle: float) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return sk_rotate(img, angle)

    return f


def shear(angle: float) -> Filter:
    return transform(AffineTransform(shear=radians(angle)))


def transform(t: AffineTransform) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return warp(img, t)

    return f

# def flip(axis):
#     def f()
