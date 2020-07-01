# pylint: disable-all
# flake8: noqa

from .base import identity
from .decorators import filter_opencv, filter_pil, filter_scikit
from .numpy import (ColorMode, bilateral_filter, color_quantization,
                    convert_color, gaussian_blur, integral, mean_filter,
                    median_filter, swirl)
from .opencv import ColorChannel, channel
from .pil import (autocontrast, brightness, contrast, equalize, hflip, invert,
                  max_filter, min_filter, mode_filter, posterize, saturation,
                  sharpness, solarize, spread, unsharpen, vflip)
from .transforms import rotate, scale, shear, transform, translate
