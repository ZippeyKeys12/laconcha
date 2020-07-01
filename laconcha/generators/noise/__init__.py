from typing import Tuple

import numpy as np

from ...image import Image


def white_noise(size: Tuple[int, int], seed: int) -> Image:
    gen = np.random.default_rng(seed)

    return Image.from_opencv((gen.random((*size, 3)) * 255).astype(np.uint8))


def gaussian_noise(size: Tuple[int, int], seed: int) -> Image:
    gen = np.random.default_rng(seed)

    return Image.from_opencv((np.clip(gen.normal(size=(*size, 3)) / 4 + .5, 0, 1) * 255).astype(np.uint8))
