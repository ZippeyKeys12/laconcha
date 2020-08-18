from typing import Tuple

import numpy as np

from ...decorators import gen_meta
from ...image import Generator, Image
from ...seed import Seed


@gen_meta(Seed)
def white_noise(seed: int) -> Generator:
    def f(size: Tuple[int, int]) -> Image:
        sample = np.random.default_rng(seed).random(size) * 255

        img = np.empty((*size, 3), dtype=np.uint8)
        img[:, :, 0] = sample
        img[:, :, 1] = sample
        img[:, :, 2] = sample

        return Image.from_scikit(img)

    return f


@gen_meta(Seed)
def gaussian_noise(seed: int) -> Generator:
    def f(size: Tuple[int, int]) -> Image:
        sample = np.clip(np.random.default_rng(seed)
                         .normal(size=size) / 4 + .5, 0, 1) * 255

        img = np.empty((*size, 3), dtype=np.uint8)
        img[:, :, 0] = sample
        img[:, :, 1] = sample
        img[:, :, 2] = sample

        return Image.from_scikit(img)

    return f
