from sklearn.cluster import MiniBatchKMeans

from ..image import Filter, Image, ImageMode


def color_quantization(n_clusters: int) -> Filter:
    def f(i: Image) -> Image:
        mode = i.mode

        if mode == ImageMode.PIL:
            img = i.as_opencv()
            mode = ImageMode.OPENCV
        else:
            img = i.img

        h, w, _ = img.shape
        X = img.reshape((h * w, 3))
        k_means = MiniBatchKMeans(n_clusters=n_clusters, random_state=0)

        labels = k_means.fit_predict(X)
        values = k_means.cluster_centers_.astype('uint8')

        res = values[labels].reshape((h, w, 3))

        if mode == ImageMode.OPENCV:
            return Image.from_opencv(res)
        elif mode == ImageMode.SCIKIT:
            return Image.from_scikit(res)

        raise Exception('what')

    return f
