# pylint: disable-all

from cv2 import saliency

import numpy as np

from ..decorators import gen_meta
from .decorators import filter_numpy

_spectral_residual = saliency.StaticSaliencySpectralResidual_create()


@gen_meta()
@filter_numpy
def spectral_residual_saliency(img: np.ndarray) -> np.ndarray:
    succ, salience = _spectral_residual.computeSaliency(img)

    if not succ:
        raise RuntimeError()

    return salience


_fine_grained = saliency.StaticSaliencyFineGrained_create()


@gen_meta()
@filter_numpy
def fine_grained_saliency(img: np.ndarray) -> np.ndarray:
    succ, salience = _fine_grained.computeSaliency(img)

    if not succ:
        raise RuntimeError()

    return salience
