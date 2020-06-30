from PIL.Image import Image as PILImage
from PIL.ImageFilter import MaxFilter, MinFilter, ModeFilter, UnsharpMask

from .decorators import Filter, filter_pil


def spread(distance: float) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.effect_spread(distance)

    return f


def unsharpen(radius: int = 2, percent: int = 150, threshold: int = 3) -> Filter:
    kernel = UnsharpMask(radius, percent, threshold)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(kernel)

    return f


def min_filter(size: int) -> Filter:
    kernel = MinFilter(size)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(kernel)

    return f


def max_filter(size: int) -> Filter:
    kernel = MaxFilter(size)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(kernel)

    return f


def mode_filter(size: int) -> Filter:
    kernel = ModeFilter(size)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(kernel)

    return f
