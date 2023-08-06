import numpy as np
import scipy
from sklearn import neighbors
from itertools import chain, combinations_with_replacement
import umap
from sklearn.neighbors import NearestNeighbors
from sklearn.manifold import LocallyLinearEmbedding, SpectralEmbedding, TSNE, Isomap
from sklearn.decomposition import PCA, KernelPCA
import NoveltyDetector as nd
from RobustHessianLLE import fast_outlier_iden_step1

class ReductionModel():
    def __init__(self, kronecker_degree = 3, n_neighbors = 24, n_components = 2, scraber = None):
        """

        :param kronecker_degree: int
        :param n_neighbors: int
        :param n_components: int
        :param scraber: the outlier identifier to be used
        """
        self.kronecker_degree = kronecker_degree
        self.k = n_neighbors
        self.n = n_components
        self.funcs = [self.fit_transform, umap.UMAP(n_neighbors=n_neighbors).fit_transform,
                 LocallyLinearEmbedding(n_components=n_components,
                                        n_neighbors=n_neighbors, method="modified").fit_transform,
                 LocallyLinearEmbedding(n_components=n_components, n_neighbors=n_neighbors, method="hessian",
                                        eigen_solver="dense").fit_transform,
                 SpectralEmbedding(n_components=n_components).fit_transform,
                 TSNE(n_components=n_components).fit_transform,
                 Isomap(n_components=n_components).fit_transform
                 ]
        self.labels = ["NPPE", "UMAP", "LLE", "Hessian", "Spectral", "TSNE", "Isomap"]

    # for kronecker computation
    def p(self, a):
        """
        A help function to compute kronecker multiplication

        :param a: array-like N*n
        :return:
        """
        (N,) = a.shape  # Unpacking fails if a is not 1-dimensional
        index_combs = chain.from_iterable((
            combinations_with_replacement(range(N), r) for r in range(1, self.kronecker_degree)))
        return [np.prod(a[list(indices)]) for indices in index_combs]

    def compute_kronecker(self, X):
        """

        :param X: array-like N*n
        :return: array-like N*(n*n)
        """
        return np.apply_along_axis(self.p, 1, X)

    def compute_hadamard(self, X):
        """

        :param X: array-like N*n
        :return: array-like N*(n*kronecker_degree)
        """
        x_hadamard = []
        N, _ = X.shape
        for i in range(N):
            x_hadamard_i = []
            # counting from kronecker_degree to 1
            for t in reversed(range(self.kronecker_degree+1)):
                if (t != 0):
                    # hadamard product of each X^i_p
                    x_hadamard_i = np.concatenate((x_hadamard_i, np.power(X[i], t)), axis=None)
            x_hadamard.append(x_hadamard_i)
        x_hadamard = np.array(x_hadamard)
        return x_hadamard

    def compute_w(self, X):
        """

        :param X:  array-like N*n matrix
        :return: array-like N*N matrix, the Neighborhood weight matrix of NPPE
        """
        N, _ = X.shape
        nbors = neighbors.kneighbors_graph(X, n_neighbors=self.k)
        W = np.zeros((N, N))
        for i, nbor_row in enumerate(nbors):
            # Get the indices of the nonzero entries in each row of the
            # neighbors matrix (which is sparse). These are the nearest
            # neighbors to the point in question. dim(Z) = [K, D]
            inds = nbor_row.indices
            Z = X[inds] - X[i]

            # Local covariance. Regularize because our data is
            # low-dimensional (K > D). dim(C) = [K, K]
            C = np.float64(np.dot(Z, Z.T))
            C += np.eye(self.k) * np.trace(C) * 0.001

            # Compute reconstruction weights
            w = scipy.linalg.solve(C, np.ones(self.k))
            W[i, inds] = w / sum(w)
        return W

    def fit_transform(self, X, offset=False, simple=True):
        """
        The fit_transform function for NPPE.

        :param X: array-like N*n matrix
        :param offset: boolean, default as False. By True the basis data matrix would be added by\
        some random value, to avoid singularity, which is achieved elsewhere, so this argument maybe redundant.

        :param simple: boolean, True=hadamard basis; False=Kronecker basis
        :return: array-like N*m matrix, the embedded data matrix

        """
        # compute diagonal D based on row sum of W
        N, n = X.shape
        W = self.compute_w(X)

        if simple:
            P = self.compute_hadamard(X)
        else:
            P = self.compute_kronecker(X)
        if offset:
            P_offset = P + np.random.rand(P.shape[0], P.shape[1])
        else:
            P_offset = P
        D = np.zeros((N, N))
        np.fill_diagonal(D, W.sum(axis=1))
        # Create sparse, symmetric matrix
        M = np.dot((D - W).T, (D - W))
        M = M.T
        A = np.dot(np.dot(P_offset.T, M), P_offset)  # X_p(D-W)X_p.T in the paper
        B = np.dot(np.dot(P_offset.T, D), P_offset)  # X_pDX_p.T in the paper
        # in case A or B is singular
        if scipy.linalg.det(A) == 0 or scipy.linalg.det(B) == 0:
            pca = PCA(n_components=min(30, n-1))
            X_pca = pca.fit_transform(X)
            return self.fit_transform(X_pca)
        vals, vecs = scipy.linalg.eigh(A, B, eigvals=(0, self.n-1))
        y = np.dot(P_offset, vecs)
        return y

    def get_reduction(self, X, cal_all = False, tag = "NPPE"):
        """
        :param X: array-like N*n
        :param cal_all: boolean, if True, return an array containing results of all given Reduction methods
        :param tag: string
        :return: y is either one reduced data-set or an array of them, according to cal_all
        """
        y = None
        if not cal_all:
            if tag == "NPPE": y = self.fit_transform(X)
            elif tag == "UMAP": y = umap.UMAP(n_neighbors=self.k).fit_transform(X)
            elif tag == "LLE" : y = LocallyLinearEmbedding(n_components=self.n,
                                            n_neighbors=self.k, method="modified").fit_transform(X)
            elif tag == "Hessian": y = LocallyLinearEmbedding(n_components=self.n,
                                                                   n_neighbors=self.k, method="hessian",
                                            eigen_solver="dense").fit_transform(X)
            elif tag == "Spectral": y = SpectralEmbedding(n_components=self.n).fit_transform(X)
            elif tag == "TSNE" : y = TSNE(n_components=self.n).fit_transform(X)
            elif tag == "Isomap": y = Isomap(n_components=self.n).fit_transform(X)
        else:
            y = []
            for f, label in zip(self.funcs, self.labels):
                y.append(f(X))
        return y

