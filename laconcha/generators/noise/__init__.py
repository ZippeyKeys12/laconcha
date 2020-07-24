from typing import Tuple

import numpy as np

from ...decorators import gen_meta
from ...image import Generator, Image
from ...seed import Seed


@gen_meta(Seed())
def white_noise(seed: int) -> Generator:
    def f(size: Tuple[int, int]) -> Image:
        gen = np.random.default_rng(seed)

        return Image.from_opencv((gen.random((*size, 3)) * 255).astype(np.uint8))

    return f


@gen_meta(Seed())
def gaussian_noise(seed: int) -> Generator:
    def f(size: Tuple[int, int]) -> Image:
        gen = np.random.default_rng(seed)

        return Image.from_opencv((np.clip(gen.normal(size=(*size, 3)) / 4 + .5, 0, 1) * 255).astype(np.uint8))

    return f
