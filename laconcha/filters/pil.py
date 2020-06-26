from PIL.Image import Image as PILImage
from PIL.ImageFilter import MaxFilter, MinFilter, ModeFilter, UnsharpMask

from .decorators import Filter, filter_pil


def spread(distance: float) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.effect_spread(distance)

    return f


def unsharpen(radius: int = 2, percent: int = 150, threshold: int = 3) -> Filter:
    mask = UnsharpMask(radius, percent, threshold)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(mask)

    return f


def min_filter(size) -> Filter:
    mask = MinFilter(size)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(mask)

    return f


def max_filter(size) -> Filter:
    mask = MaxFilter(size)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(mask)

    return f


def mode_filter(size) -> Filter:
    mask = ModeFilter(size)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(mask)

    return f
