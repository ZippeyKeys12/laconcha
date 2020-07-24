from PIL import ImageChops
from PIL.Image import Image as PILImage

from ..decorators import gen_meta
from ..image import Operator
from ..ranges import Range
from .decorators import operator_pil


@gen_meta()
def add() -> Operator:
    return operator_pil(ImageChops.add)


@gen_meta()
def add_modulo() -> Operator:
    return operator_pil(ImageChops.add_modulo)


@gen_meta()
def overlay() -> Operator:
    return operator_pil(ImageChops.overlay)


@gen_meta()
def screen() -> Operator:
    return operator_pil(ImageChops.screen)


@gen_meta()
def soft_light() -> Operator:
    return operator_pil(ImageChops.soft_light)


@gen_meta()
def subtract() -> Operator:
    return operator_pil(ImageChops.subtract)


@gen_meta()
def subtract_modulo() -> Operator:
    return operator_pil(ImageChops.subtract_modulo)


@gen_meta()
def darker() -> Operator:
    return operator_pil(ImageChops.darker)


@gen_meta()
def difference() -> Operator:
    return operator_pil(ImageChops.difference)


@gen_meta()
def hard_light() -> Operator:
    return operator_pil(ImageChops.hard_light)


@gen_meta()
def lighter() -> Operator:
    return operator_pil(ImageChops.lighter)


@gen_meta(Range(0.0, 1, default=1))
def blend(alpha: float) -> Operator:
    @operator_pil
    def f(a: PILImage, b: PILImage) -> PILImage:
        return ImageChops.blend(a, b, alpha)

    return f
