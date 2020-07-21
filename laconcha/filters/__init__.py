# pylint: disable-all
# flake8: noqa

from .base import identity
from .cropping import bottom, crop, fit, left, right, top
from .decorators import filter_numpy, filter_opencv, filter_pil, filter_scikit
from .designs import swirl_flower
from .kaleidoscope import hmirror, oct_mirror, quad_mirror, vmirror
from .numpy import (bilateral_filter, color_quantization, curve, gaussian_blur,
                    integral, mean_filter, median_filter, shuffle, swirl)
from .opencv import ColorChannel, get_channel
from .pil import (autocontrast, brightness, contrast, equalize, hflip, invert,
                  max_filter, min_filter, mode_filter, posterize, saturation,
                  sharpness, solarize, spread, unsharpen, vflip)
from .scikit import ColorMode, convert_color
from .tiling import mirror_tile, tile
from .transforms import rotate, scale, shear, transform, translate
