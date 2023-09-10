from ..image import Filter, Image


def funnel(*fs: Filter) -> Filter:
    fs = tuple(reversed(fs))

    def f(img: Image) -> Image:
        rfs = list(fs)
        while len(rfs) > 0:
            img = rfs[-1](img)
            rfs.pop()

        return img

    return f
