from typing import Callable, Tuple

import numpy as np

from ..image import Generator, Image
from ..util import safe_divide

Func = Callable[[int, int], int]


def from_function(func: Func) -> Generator:
    def f(size: Tuple[int, int]) -> Image:
        img = np.empty((*size, 3), dtype=np.int16)
        h, w = size
        cx, cy = w // 2, h // 2

        for y in range(h):
            for x in range(w):
                z = np.clip(func(x - cx, y - cy),
                            np.int16.a_min, np.int16.a_max)
                img[y][x] = (z, z, z)

        if np.min(img) < 0:
            img -= np.min(img)
        if np.max(img) > 255:
            img = 255 * safe_divide(img, np.max(img))

        return Image.from_opencv(img.astype(np.uint8))

    return f


def from_rgb_functions(f1: Func, f2: Func, f3: Func) -> Generator:
    def f(size: Tuple[int, int]) -> Image:
        img = np.empty((*size, 3), dtype=np.int16)
        h, w = size
        cx, cy = w // 2, h // 2

        for y in range(h):
            for x in range(w):
                ax = x - cx
                ay = y - cy

                r = np.clip(f1(ax, ay), np.int16.a_min, np.int16.a_max)
                g = np.clip(f2(ax, ay), np.int16.a_min, np.int16.a_max)
                b = np.clip(f3(ax, ay), np.int16.a_min, np.int16.a_max)
                img[y][x] = (r, g, b)

        if np.min(img) < 0:
            img -= np.min(img)
        if np.max(img) > 255:
            img = 255 * safe_divide(img, np.max(img))

        return Image.from_scikit(img.astype(np.uint8))

    return f
