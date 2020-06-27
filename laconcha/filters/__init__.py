# pylint: disable-all
# flake8: noqa

from .decorators import filter_opencv, filter_pil, filter_scikit
from .opencv import (ColorChannel, ColorMode, bilateral_filter, channel,
                     color_quantization, convert_color, gaussian_blur,
                     mean_filter, median_filter)
from .pil import spread
