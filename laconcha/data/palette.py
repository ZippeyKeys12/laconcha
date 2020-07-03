from typing import Callable

import numpy as np
from sklearn import cluster

from ..image import Image


def color_palette(n_clusters: int) -> Callable[[np.ndarray], cluster.KMeans]:
    def f(img: Image) -> cluster.KMeans:
        h, w, _ = img.as_scikit().shape
        X = img.as_scikit().reshape((h * w, 3))
        k_means = cluster.KMeans(n_clusters=n_clusters, random_state=0)
        k_means.fit(X)

        return k_means

    return f
