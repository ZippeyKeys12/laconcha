from PIL import ImageChops, ImageOps
from PIL.Image import Image as PILImage
from PIL.ImageEnhance import Brightness, Color, Contrast, Sharpness
from PIL.ImageFilter import MaxFilter, MinFilter, ModeFilter, UnsharpMask

from .decorators import Filter, filter_pil
from ..decorators import gen_meta
from ..ranges import Range


@gen_meta(Range(0, 16, default=3))
def spread(distance: float) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.effect_spread(distance)

    return f


@gen_meta(Range(0, 8, default=2), Range(0, 201, default=150), Range(0, 11, default=3))
def unsharpen(radius: int = 2, percent: int = 150, threshold: int = 3) -> Filter:
    kernel = UnsharpMask(radius, percent, threshold)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(kernel)

    return f


@gen_meta(Range(1, 16, 2, 9))
def min_filter(size: int) -> Filter:
    kernel = MinFilter(size)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(kernel)

    return f


@gen_meta(Range(1, 16, 2, 9))
def max_filter(size: int) -> Filter:
    kernel = MaxFilter(size)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(kernel)

    return f


@gen_meta(Range(1, 16, 2, 9))
def mode_filter(size: int) -> Filter:
    kernel = ModeFilter(size)

    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.filter(kernel)

    return f


@gen_meta(Range(0.0, 2, default=1))
def brightness(factor: float) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return Brightness(img).enhance(factor)

    return f


@gen_meta(Range(0.0, 2, default=1))
def contrast(factor: float) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return Contrast(img).enhance(factor)

    return f


@gen_meta(Range(0.0, 2, default=1))
def saturation(factor: float) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return Color(img).enhance(factor)

    return f


@gen_meta(Range(0.0, 2, default=1))
def sharpness(factor: float) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return Sharpness(img).enhance(factor)

    return f


@gen_meta()
@filter_pil
def invert(img: PILImage) -> PILImage:
    return ImageChops.invert(img)


@gen_meta(Range(0, 50))
def autocontrast(cutoff: float = 0) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return ImageOps.autocontrast(img, cutoff)

    return f


@gen_meta()
def equalize(mask=None) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return ImageOps.equalize(img, mask)

    return f


@gen_meta()
@filter_pil
def vflip(img: PILImage) -> PILImage:
    return ImageOps.flip(img)


@gen_meta()
@filter_pil
def hflip(img: PILImage) -> PILImage:
    return ImageOps.mirror(img)


@gen_meta(Range(1, 9, default=8))
def posterize(bits: int) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return ImageOps.posterize(img, bits)

    return f


@gen_meta(Range(0, 256, default=128))
def solarize(threshold: int = 128) -> Filter:
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return ImageOps.solarize(img, threshold)

    return f
