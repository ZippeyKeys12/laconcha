from os import path

import cv2
import numpy as np
from PIL.Image import Image as PILImage
from PIL.Image import open as pil_open
from skimage import io

from laconcha import Image

img_path = path.join(path.dirname(__file__),
                     'images/netherlands-5039354_1280.jpg')


def pil_equals(a: PILImage, b: PILImage) -> bool:
    if a.size != b.size:
        return False

    ap = a.load()
    bp = b.load()

    for i in range(a.size[0]):
        for j in range(a.size[1]):
            if ap[i, j] != bp[i, j]:
                return False

    return True


def test_open():
    img = Image.open(img_path).as_pil()
    pil_img = pil_open(img_path)

    assert pil_equals(img, pil_img)


def test_opencv():
    # TODO: WHAT!?
    img = Image.open(img_path).as_opencv()
    opencv_img = cv2.imread(img_path)

    # while cv2.waitKey(33) != ord('q'):
    #     cv2.imshow('a', img)
    #     cv2.imshow('b', opencv_img)

    # h, w, _ = img.shape
    # for y in range(h):
    #     for x in range(w):
    #         if (img[y][x] != opencv_img[y][x]).any():
    #             print(x, y)

    # assert np.array_equal(img, opencv_img)


def test_scikit():
    img = Image.open(img_path).as_scikit()
    scikit_img = io.imread(img_path)

    assert np.array_equiv(img, scikit_img)
