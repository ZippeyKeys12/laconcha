from PIL.Image import Image as PILImage
from PIL.ImageEnhance import Brightness, Color, Contrast, Sharpness
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


def brightness(factor: float) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return Brightness(img).enhance(factor)

    return f


def contrast(factor: float) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return Contrast(img).enhance(factor)

    return f


def saturation(factor: float) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return Color(img).enhance(factor)

    return f


def sharpness(factor: float) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return Sharpness(img).enhance(factor)

    return f
