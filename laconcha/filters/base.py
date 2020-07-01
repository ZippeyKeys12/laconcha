from PIL.Image import Image as PILImage

from .decorators import filter_pil


def identity():
    @filter_pil
    def f(img: PILImage) -> PILImage:
        return img.copy()

    return f
