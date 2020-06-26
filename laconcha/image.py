from __future__ import annotations

from enum import IntEnum, auto
from typing import Callable, Iterable, Optional, Tuple, Union

import cv2
import numpy as np
from PIL.Image import Image as PILImage
from PIL.Image import fromarray as pil_fromarray
from PIL.Image import open as pil_open

RawImage = Union[np.ndarray, PILImage]


class ImageMode(IntEnum):
    OPENCV = auto()
    PIL = auto()
    SCIKIT = auto()


class Image:
    __slots__ = ['mode', 'img', 'size']

    def __init__(self, size: Tuple[int, int], init: bool = True):
        self.size = size

        if init:
            self.mode = ImageMode.OPENCV
            self.img = np.zeros((*size, 3), dtype=np.uint8)

    @staticmethod
    def open(fp):
        img = pil_open(fp)
        img.load()
        return Image.from_pil(img)

    @staticmethod
    def from_opencv(img: np.ndarray) -> Image:
        res = Image(img.shape[:2], init=False)
        res.mode = ImageMode.OPENCV
        res.img = img
        return res

    @staticmethod
    def from_pil(img: PILImage) -> Image:
        res = Image(img.size[::-1], init=False)
        res.mode = ImageMode.PIL
        res.img = img
        return res

    @staticmethod
    def from_scikit(img: np.ndarray) -> Image:
        res = Image(img.shape[:2], init=False)
        res.mode = ImageMode.SCIKIT
        res.img = img
        return res

    def as_opencv(self) -> np.ndarray:
        if self.mode == ImageMode.PIL:
            self.img = cv2.cvtColor(np.asarray(self.img), cv2.COLOR_RGB2BGR)

        elif self.mode == ImageMode.SCIKIT:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)

        return self.img

    def as_pil(self) -> PILImage:
        if self.mode == ImageMode.OPENCV:
            self.img = pil_fromarray(
                cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))

        elif self.mode == ImageMode.SCIKIT:
            self.img = pil_fromarray(self.img)

        return self.img

    def as_scikit(self) -> np.ndarray:
        if self.mode == ImageMode.OPENCV:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        elif self.mode == ImageMode.PIL:
            self.img = np.asarray(self.img)

        return self.img

    def apply_filter(self, f: Filter):
        res = f(self)
        self.mode = res.mode
        self.img = res.img
        self.size = res.size

    def apply_filters(self, fs: Iterable[Filter]):
        for f in fs:
            self.apply_filter(f)

    def show(self, title: Optional[str] = None):
        self.as_pil().show(title)

    def save(self, fp):
        self.as_pil().save(fp)


Filter = Callable[[Image], Image]
Operator = Callable[[Image, Image], Image]
