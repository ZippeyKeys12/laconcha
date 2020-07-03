from math import cos, e, log10, pi, sin
from math import sqrt as square_root  # noqa
from typing import Callable

Curve = Callable[[float], float]


def quadratic(x: float) -> float:
    return x ** 2


def cubic(x: float) -> float:
    return x ** 3


def exponential(x: float) -> float:
    return e**(10 * (x - 1))


def sine(x: float) -> float:
    return sin(x * pi / 2)


def cosine(x: float) -> float:
    return 1 - cos(x * pi / 2)


def logarithm(x: float) -> float:
    return -log10(1 - .9 * x)


def inverse(x: float) -> float:
    return x / (2 - x)


def circular(x: float) -> float:
    return 1 - square_root(1 - x**2)
