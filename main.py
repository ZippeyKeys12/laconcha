import json
import os
import random as rand
from math import sin, tan
from typing import Callable, List, Tuple

import numpy as np

from a import generate_img
from laconcha import ColorChannel, Image
from laconcha.curves import (circular, cosine, cubic, exponential, inverse,
                             logarithm, quadratic, sine, smooth_step,
                             smoother_step, smoothest_step, square_root)
from laconcha.filters import (ColorMode, autocontrast, bilateral_filter,
                              bottom, brightness, color_quantization, contrast,
                              convert_color, crop, curve, equalize, fit,
                              gaussian_blur, get_channel, hflip, hmirror,
                              integral, invert, left, max_filter, mean_filter,
                              median_filter, min_filter, mode_filter,
                              oct_mirror, posterize, quad_mirror, right,
                              rotate, saturation, scale, sharpness, shear,
                              shuffle, solarize, spread, swirl, swirl_flower,
                              top, transform, translate, unsharpen, vflip,
                              vmirror)
from laconcha.generators import (from_function, from_rgb_functions,
                                 gaussian_noise, maurer_rose, solid_color,
                                 white_noise)
from laconcha.operators import (add, add_modulo, blend, darker, difference,
                                hard_light, lighter, overlay, screen,
                                set_channel, soft_light, subtract,
                                subtract_modulo)
from laconcha.seed import get_seed
from laconcha.util import hex_to_rgb

HEIGHT, WIDTH = 1024, 1024
# HEIGHT, WIDTH = 400, 400

seed = input('Seed? ')

if seed == '':
    seed = get_seed()

print(f'Seed: {seed}')
rand.seed(seed)


MIN_DEPTH = 1
MAX_DEPTH = 5

functions = [
    lambda x, y: 255 * (sin(x) / 2 + .5),
    lambda x, y: 255 * (sin(y) / 2 + .5),
    lambda x, y: 255 * (sin(x) / 2 + .5) * (sin(y) / 2 + .5),
    lambda x, y: x**2 % 255,
    lambda x, y: y**2 % 255,
    lambda x, y: (x**2 + y**2) % 255,
    lambda x, y: tan(x) % 255,
    lambda x, y: tan(y) % 255,
    lambda x, y: tan(x) % 255 + tan(y) % 255,
]


def function(size, _):
    return from_function(rand.choice(functions))(size)


def rgb_function(size, _):
    return from_rgb_functions(*rand.choices(functions, k=3))(size)


files = [f for f in os.listdir('test_images') if f.endswith('.jpg')]


def file(size, _):
    return fit(size)(Image.open('test_images/' + rand.choice(files)))


# TODO: Weight choices
generators = [
    # file,
    # function,
    # rgb_function,
    # gaussian_noise,
    # white_noise
    (1, solid_color, lambda: [
        rand.choices(range(256), k=3)
    ])
    (2, maurer_rose, lambda: [
        *rand.choice([
            (2, 39),
            (3, 47),
            (4, 31),
            (5, 97),
            (6, 71),
            (7, 19)
        ]),
        rand.randint(min(HEIGHT, WIDTH) // 2, max(HEIGHT, WIDTH)),
        rand.choices(range(256), k=3),
        rand.choices(range(256), k=3)
    ]),
    (3, lambda: generate_img, lambda: [])
]

weights = [i[0] for i in generators]
generators = [i[1:] for i in generators]

filters: List[Tuple[Callable, Callable]] = [
    (autocontrast, lambda h, w: [
        rand.randint(0, 49)
    ]),
    (bilateral_filter, lambda h, w: [
        rand.randint(1, 15),
        rand.randint(0, 100),
        rand.randint(0, 100)
    ]),
    # (bottom, lambda h, w: [
    #     rand.randint(0, h)
    # ]),
    (brightness, lambda h, w: [
        2 * rand.random()
    ]),
    (get_channel, lambda h, w: [
        rand.choice(list(ColorChannel))
    ]),
    (color_quantization, lambda h, w: [
        rand.randint(2, 16)
    ]),
    (contrast, lambda h, w: [
        2 * rand.random()
    ]),
    (convert_color, lambda h, w: [
        list(ColorMode),
        list(ColorMode)
    ]),
    # (crop, lambda h, w: [
    #     (rand.randint(0, h),
    #      rand.randint(0, w))
    # ]),
    (curve, lambda h, w: [
        rand.choice([
            circular,
            cosine,
            cubic,
            exponential,
            inverse,
            logarithm,
            sine,
            smooth_step,
            smoother_step,
            smoothest_step,
            square_root,
            quadratic
        ])
    ]),
    (equalize, lambda h, w: []),
    # (fit, lambda h, w: [
    #     (rand.randint(0, h),
    #      rand.randint(0, w))
    # ]),
    (gaussian_blur, lambda h, w: [
        (rand.randrange(1, 8, 2),
         rand.randrange(1, 8, 2)),
        10 * rand.random()
    ]),
    (lambda: hflip, lambda h, w: []),
    (lambda: hmirror, lambda h, w: []),
    # 'Integral': (integral, lambda h, w: []),
    (lambda: invert, lambda h, w: []),
    # (left, lambda h, w: [
    #     rand.randint(0, w)
    # ]),
    (max_filter, lambda h, w: [
        rand.randrange(1, 16, 2)
    ]),
    (mean_filter, lambda h, w: [
        (rand.randint(1, 7),
         rand.randint(1, 7))
    ]),
    (median_filter, lambda h, w: [
        rand.randrange(1, 16, 2)
    ]),
    (min_filter, lambda h, w: [
        rand.randrange(1, 16, 2)
    ]),
    (mode_filter, lambda h, w: [
        rand.randrange(1, 16, 2)
    ]),
    (lambda: oct_mirror, lambda h, w: []),
    (posterize, lambda h, w: [
        rand.randint(2, 8)
    ]),
    (lambda: quad_mirror, lambda h, w: []),
    # (right, lambda h, w: [
    #     rand.randint(0, w)
    # ]),
    (rotate, lambda h, w: [
        360 * rand.random()
    ]),
    (saturation, lambda h, w: [
        2 * rand.random()
    ]),
    (scale, lambda h, w: [
        9 * rand.random() + 1
    ]),
    (sharpness, lambda h, w: [
        2 * rand.random()
    ]),
    (shuffle, lambda h, w: [
        rand.randint(0, int(16 * '1', base=2))
    ]),
    (solarize, lambda h, w: [
        rand.randint(0, 255)
    ]),
    (spread, lambda h, w: [
        rand.randint(10, 50)
    ]),
    (swirl, lambda h, w: [
        (w // 2, h // 2),
        200 * rand.random() - 100,
        max(h, w)
    ]),
    (unsharpen, lambda h, w: [
        rand.randint(1, 15)
    ]),
    (lambda: vflip, lambda h, w: []),
    (lambda: vmirror, lambda h, w: [])
]


def rblend(a, b):
    return blend(rand.random())(a, b)


def rset_channel(a, b):
    return set_channel(rand.choice(list(ColorChannel)))(a, b)


operators = [
    (2, add()),
    (2, add_modulo()),
    (2, rblend),
    (2, darker()),
    (2, difference()),
    (2, hard_light()),
    (2, lighter()),
    (2, overlay()),
    (2, screen()),
    (2, rset_channel),
    (2, soft_light()),
    (2, subtract()),
    (2, subtract_modulo())
]


def get_image(depth: int = 1) -> Image:
    if depth == 5:
        return get_filtered()

    if depth > 2 and rand.random() < .25:
        return get_generator()

    o = rand.choice(operators)

    # print(o[1].__name__)

    i = o[1](*[get_image(depth + 1) for _ in range(o[0])]).as_scikit()
    num_colors = len(np.unique(i.reshape(i.shape[0] * i.shape[1], 3), axis=0))

    if num_colors == 1:
        return get_image()

    return Image.from_scikit(i)


def get_filtered(depth: int = 1) -> Image:
    if depth == MAX_DEPTH:
        return get_generator()

    if depth > MIN_DEPTH and rand.random() < .25:
        return get_generator()

    f = rand.choice(filters)

    # print(f[0].__name__)

    return f[0](*f[1](HEIGHT, WIDTH))(get_filtered(depth + 1))


def get_generator() -> Image:
    g = rand.choices(generators, weights=weights)

    # print(g.__name__)

    return g[1](*g[2]())((HEIGHT, WIDTH))


with open('1000.json', 'r') as f:
    palettes = json.load(f)

palette = rand.choice(palettes)

N = 5

# tru_img = rand.choice([
#     # hmirror(),
#     quad_mirror(),
#     oct_mirror(),
#     flower(rand.choice([
#         add(),
#         add_modulo(),
#         darker(),
#         difference(),
#         hard_light(),
#         lighter(),
#         overlay(),
#         screen(),
#         soft_light(),
#         subtract(),
#         subtract_modulo()
#     ]), 500, max(HEIGHT, WIDTH))
# ])(get_image())
tru_img = get_image()

img = tru_img.as_scikit()
colors, counts = np.unique(img.reshape(
    img.shape[0] * img.shape[1], 3), return_counts=True, axis=0)

if len(colors) > N:
    there = convert_color(ColorMode.RGB, ColorMode.LAB)
    back = convert_color(ColorMode.LAB, ColorMode.RGB)
    img = back(color_quantization(N)(there(tru_img))).as_scikit()
    colors, counts = np.unique(img.reshape(
        img.shape[0] * img.shape[1], 3), return_counts=True, axis=0)


indices = np.argsort(counts)
for i in range(len(colors)):
    mask = np.where((img == colors[indices[i]]).all(axis=2))
    img[mask] = hex_to_rgb(palette[i])

img = mode_filter(7)(Image.from_scikit(img))

# img = tru_img

img.show('Palettized')

save = input('Save? ')
if save.strip().lower() in ['y', 'yes']:
    img.save(f'palettized/{seed}.jpg')
