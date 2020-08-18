from typing import Tuple

import numpy as np

from ..decorators import gen_meta
from ..image import Filter, Image
from ..ranges import Range
from .decorators import filter_numpy
from .kaleidoscope import hattach, hflip, vattach, vflip


@gen_meta((Range(1, 11), Range(1, 11)))
def tile(transform: Tuple[int, int]) -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        return np.tile(img, (*transform, 1))

    return f


@gen_meta((Range(1, 11), Range(1, 11)))
def mirror_tile(size: Tuple[int, int]) -> Filter:
    def f(img: Image) -> Image:
        height, width = size

        nimg = img

        vimg = vflip(img)
        for i in range(1, height):
            if i % 2 == 0:
                img = vattach(img, nimg)
            else:
                img = vattach(img, vimg)

        nimg = img
        himg = hflip(img)
        for i in range(1, width):
            if i % 2 == 0:
                img = hattach(img, nimg)
            else:
                img = hattach(img, himg)

        return img

    return f
