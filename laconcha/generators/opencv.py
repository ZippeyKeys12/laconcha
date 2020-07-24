from typing import Tuple

import numpy as np

from ..decorators import gen_meta
from ..image import Generator, Image
from ..util import RGBColor


@gen_meta(RGBColor)
def solid_color(color: RGBColor) -> Generator:
    def f(size: Tuple[int, int]) -> Image:
        return Image.from_opencv(np.tile(color, size[0] * size[1]).reshape(*size, 3).astype(np.uint8))

    return f
