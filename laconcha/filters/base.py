from PIL.Image import Image as PILImage

from ..decorators import gen_meta
from .decorators import filter_pil


@gen_meta()
@filter_pil
def identity(img: PILImage) -> PILImage:
    return img.copy()
