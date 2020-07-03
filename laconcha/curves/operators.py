from .base import Curve


def invert(c: Curve) -> Curve:
    return lambda t: 1 - c(1 - t)


def lerp(a: Curve, b: Curve) -> Curve:
    return lambda t: (1 - t) * a(t) + t * b(t)
