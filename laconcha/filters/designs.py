from ..image import Filter, Image, Operator
from .numpy import swirl


def swirl_flower(blend: Operator, strength: float = 1, radius: float = 100) -> Filter:
    def f(img: Image) -> Image:
        h, w = img.size
        a = swirl((w // 2, h // 2), strength, radius)(img)
        b = swirl((w // 2, h // 2), -strength, radius)(img)
        return blend(a, b)

    return f
