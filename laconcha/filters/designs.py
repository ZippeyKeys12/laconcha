from ..decorators import gen_meta
from ..image import Filter, Image, Operator
from ..operators.blend_modes import (add, add_modulo, darker, difference,
                                     hard_light, lighter, overlay, screen,
                                     soft_light, subtract, subtract_modulo)
from .numpy import swirl
from ..ranges import Range


@gen_meta(
    [
        add(),
        add_modulo(),
        darker(),
        difference(),
        hard_light(),
        lighter(),
        overlay(),
        screen(),
        soft_light(),
        subtract(),
        subtract_modulo()
    ],
    Range(0.0, 100),
    Range(1.0, 1024)
)
def swirl_flower(blend: Operator, strength: float = 1, radius: float = 100) -> Filter:
    def f(img: Image) -> Image:
        a = swirl(strength, radius)(img)
        b = swirl(-strength, radius)(img)
        return blend(a, b)

    return f
