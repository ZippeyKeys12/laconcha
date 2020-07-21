from typing import Callable, Tuple

import numpy as np

from ..image import Generator, Image

Func = Callable[[int, int], int]


def from_function(func: Func) -> Generator:
    def f(size: Tuple[int, int]) -> Image:
        h, w = size
        img = np.empty((*size, 3), dtype=np.uint8)

        for y in range(h):
            for x in range(w):
                z = np.clip(func(x, y), 0, 255)
                img[y][x] = (z, z, z)

        return Image.from_opencv(img)

    return f


def from_rgb_functions(f1: Func, f2: Func, f3: Func) -> Generator:
    def f(size: Tuple[int, int]) -> Image:
        h, w = size
        img = np.empty((*size, 3), dtype=np.uint8)

        for y in range(h):
            for x in range(w):
                r = np.clip(f1(x, y), 0, 255)
                g = np.clip(f2(x, y), 0, 255)
                b = np.clip(f3(x, y), 0, 255)
                img[y][x] = (r, g, b)

        return Image.from_scikit(img)

    return f
