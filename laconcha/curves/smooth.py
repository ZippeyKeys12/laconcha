def smooth_step(x: float) -> float:
    return -2 * x**3 + 3 * x**2


def smoother_step(x: float) -> float:
    return 6 * x**5 - 15 * x**4 + 10 * x**3


def smoothest_step(x: float) -> float:
    return -20 * x**7 + 70 * x**6 - 84 * x**5 + 35 * x**4
