import numpy as np

from ..image import Image
from ..operators import hattach, vattach
from .cropping import left, top
from .decorators import filter_numpy
from .pil import hflip, vflip


def vmirror(img: Image) -> Image:
    h, _ = img.size
    img = top(h // 2)(img)
    return vattach(img, vflip(img))


def hmirror(img: Image) -> Image:
    _, w = img.size
    img = left(w // 2)(img)
    return hattach(img, hflip(img))


@filter_numpy
def diag_mirror(img: np.ndarray) -> np.ndarray:
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


def quad_mirror(img: Image) -> Image:
    return vmirror(hmirror(img))


def oct_mirror(img: Image) -> Image:
    return quad_mirror(diag_mirror(img))
