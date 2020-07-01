from PIL import ImageChops
from PIL.Image import Image as PILImage

from ..image import Operator
from .decorators import operator_pil


def add() -> Operator:
    return operator_pil(ImageChops.add)


def add_modulo() -> Operator:
    return operator_pil(ImageChops.add_modulo)


def overlay() -> Operator:
    return operator_pil(ImageChops.overlay)


def screen() -> Operator:
    return operator_pil(ImageChops.screen)


def soft_light() -> Operator:
    return operator_pil(ImageChops.soft_light)


def subtract() -> Operator:
    return operator_pil(ImageChops.subtract)


def subtract_modulo() -> Operator:
    return operator_pil(ImageChops.subtract_modulo)


def darker() -> Operator:
    return operator_pil(ImageChops.darker)


def difference() -> Operator:
    return operator_pil(ImageChops.difference)


def hard_light() -> Operator:
    return operator_pil(ImageChops.hard_light)


def lighter() -> Operator:
    return operator_pil(ImageChops.lighter)


def blend(alpha: float) -> Operator:
    @operator_pil
    def f(a: PILImage, b: PILImage) -> PILImage:
        return operator_pil(ImageChops.blend(a, b, alpha))

    return f
