import numpy as np

from ..image import Filter, Image
from ..operators import hattach, vattach
from .cropping import left, top
from .decorators import filter_numpy
from .pil import hflip, vflip


def vmirror() -> Filter:
    def f(img: Image) -> Image:
        h, _ = img.size
        img = top(h // 2)(img)
        return vattach()(img, vflip()(img))

    return f


def hmirror() -> Filter:
    def f(img: Image) -> Image:
        _, w = img.size
        img = left(w // 2)(img)
        return hattach()(img, hflip()(img))

    return f


def diag_mirror() -> Filter:
    @filter_numpy
    def f(img: np.ndarray) -> np.ndarray:
        h, w, _ = img.shape

        if h != w:
            raise ValueError('Must be square image')

        new_image = np.empty_like(img)

        for y in range(h):
            for x in range(w):
                if x < y:
                    new_image[y][x] = img[x][y]
                else:
                    new_image[y][x] = img[y][x]

        return new_image

    return f


def quad_mirror() -> Filter:
    def f(img: Image) -> Image:
        return vmirror()(hmirror()(img))

    return f


def oct_mirror() -> Filter:
    def f(img: Image) -> Image:
        return quad_mirror()(diag_mirror()(img))

    return f
