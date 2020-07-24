from math import cos, radians, sin
from typing import Tuple

from PIL import ImageDraw
from PIL.Image import new as pil_new

from ..decorators import gen_meta
from ..image import Generator, Image
from ..ranges import Range
from ..util import RGBColor


@gen_meta(
    Range(1, 11, default=2),
    Range(1, 101, default=39),
    Range(1, 1001, default=300),
    RGBColor,
    RGBColor
)
def maurer_rose(n: int, d: int, radius: int, color1: RGBColor, color2: RGBColor) -> Generator:
    def f(size: Tuple[int, int]) -> Image:
        height, width = size
        img = pil_new('RGB', (width, height))
        cx, cy = width // 2, height // 2

        x = cx
        y = cy
        coords = []

        draw = ImageDraw.Draw(img)
        for theta in range(361):
            coords.append((x, y))

            k = radians(theta * d)
            r = radius * sin(n * k)
            x = cx + int(-r * cos(k))
            y = cy + int(-r * sin(k))
        draw.line(coords, fill=color1, width=2)

        coords.clear()
        for theta in range(361):
            coords.append((x, y))

            k = radians(theta)
            r = radius * sin(n * k)
            x = cx + int(r * cos(k))
            y = cy + int(-r * sin(k))
        draw.line(coords, fill=color2, width=5)

        return Image.from_pil(img)

    return f
