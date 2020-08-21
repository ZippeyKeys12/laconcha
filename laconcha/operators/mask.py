from skimage.util import img_as_float64

from ..decorators import gen_meta
from ..image import Image


@gen_meta()
def masking(fore: Image, back: Image, mask: Image) -> Image:
    if fore.size != back.size or back.size != mask.size:
        raise ValueError('Images must be of same dimensions')

    f = img_as_float64(fore.as_scikit())
    b = img_as_float64(back.as_scikit())
    m = img_as_float64(mask.as_scikit())

    print('mask')

    return Image.from_scikit(m * f + (1 - m) * b)
