"""K-Means clustering implemented from scratch with NumPy.

The algorithm follows the standard Lloyd's method:
1. Initialise k centroids using the k-means++ strategy.
2. Assign every point to the closest centroid.
3. Recompute each centroid as the mean of its assigned points.
4. Repeat steps 2-3 until assignments stop changing (or max iterations reached).
"""

import numpy as np


class KMeans:
    """A from-scratch implementation of the K-Means clustering algorithm."""

    def __init__(self, n_clusters=3, max_iter=300, random_state=None):
        if n_clusters < 1:
            raise ValueError("n_clusters must be at least 1")
        if max_iter < 1:
            raise ValueError("max_iter must be at least 1")
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids_ = None
        self.labels_ = None
        self.inertia_ = None
        self.n_iter_ = None

    def _rng(self):
        return np.random.default_rng(self.random_state)

    def _init_centroids_kmeans_plus_plus(self, X, rng):
        """Initialise centroids far apart from each other (k-means++)."""
        n_samples = X.shape[0]
        centroids = np.empty((self.n_clusters, X.shape[1]))
        first_idx = rng.integers(0, n_samples)
        centroids[0] = X[first_idx]
        nearest_dist2 = np.full(n_samples, np.inf)
        for c in range(1, self.n_clusters):
            dist2 = ((X - centroids[c - 1]) ** 2).sum(axis=1)
            nearest_dist2 = np.minimum(nearest_dist2, dist2)
            probs = nearest_dist2 / nearest_dist2.sum()
            centroids[c] = X[rng.choice(n_samples, p=probs)]
        return centroids

    @staticmethod
    def _assign(X, centroids):
        """Assign each point to its nearest centroid; return labels and squared distances."""
        diff = X[:, None, :] - centroids[None, :, :]
        dists = (diff ** 2).sum(axis=2)
        labels = np.argmin(dists, axis=1)
        return labels, dists[np.arange(X.shape[0]), labels]

    def fit(self, X):
        """Cluster the data and store centroids, labels and inertia on the instance."""
        X = self._validate_input(X)
        n_samples, n_features = X.shape
        if self.n_clusters > n_samples:
            raise ValueError(
                f"n_clusters ({self.n_clusters}) cannot exceed the number of samples ({n_samples})"
            )
        rng = self._rng()
        centroids = self._init_centroids_kmeans_plus_plus(X, rng)
        labels, dists = self._assign(X, centroids)
        self.n_iter_ = 1
        while self.n_iter_ < self.max_iter:
            new_centroids = np.empty_like(centroids)
            for c in range(self.n_clusters):
                members = X[labels == c]
                if len(members) == 0:
                    farthest_idx = int(np.argmax(dists))
                    new_centroids[c] = X[farthest_idx]
                else:
                    new_centroids[c] = members.mean(axis=0)
            new_labels, new_dists = self._assign(X, new_centroids)
            self.n_iter_ += 1
            if np.array_equal(new_labels, labels):
                labels, dists = new_labels, new_dists
                centroids = new_centroids
                break
            labels, dists, centroids = new_labels, new_dists, new_centroids
        self.centroids_ = centroids
        self.labels_ = labels
        self.inertia_ = float(dists.sum())
        return self

    def predict(self, X):
        """Return the cluster label for each row of X."""
        X = self._validate_input(X)
        if self.centroids_ is None:
            raise RuntimeError("fit() must be called before predict()")
        labels, _ = self._assign(X, self.centroids_)
        return labels

    @staticmethod
    def _validate_input(X):
        """Validate and normalise the input matrix; raise helpful errors otherwise."""
        arr = np.asarray(X, dtype=float)
        if arr.ndim != 2:
            raise ValueError("X must be a 2-dimensional array of shape (n_samples, n_features)")
        if arr.shape[0] == 0:
            raise ValueError("X must contain at least one sample")
        if arr.shape[1] == 0:
            raise ValueError("X must contain at least one feature")
        if np.isnan(arr).any():
            raise ValueError("X contains NaN values; clean the data before clustering")
        if np.isinf(arr).any():
            raise ValueError("X contains infinite values; clean the data before clustering")
        return arr


def elbow_wcss(X, k_range, max_iter=100, random_state=None):
    """Compute within-cluster sum of squares for each k, to support elbow selection."""
    return {
        k: KMeans(n_clusters=k, max_iter=max_iter, random_state=random_state)
        .fit(X)
        .inertia_
        for k in k_range
    }
