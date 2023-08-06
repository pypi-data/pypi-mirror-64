from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition.pca import *
import numpy as np

# paper: 'Robust Hessian Locally Linear Embedding Techniques for High-Dimensional Data' by Xing et al.
def fast_outlier_iden_step1(X, k=None, tol=1e-2, max_iter=1000):
    """
    The fast outlier identifying algorithm according to section 4.2 in paper Robust Hessian LLE.
    Following implements the first step of 4.2.

    :param X: array-like N*n matrix
    :param tol: float
    :param max_iter: int
    :return: (N*N, N*n), the array-like N*N weight matrix indicating outliers, and\
    the N*n matrix, the mean coordinate of k Nearest Neighbors of each x_i in X.

    """
    N, n = X.shape
    if k is None: k = 2*n
    nbrs = NearestNeighbors(n_neighbors=k + 1, algorithm='ball_tree').fit(X)
    distances, indices = nbrs.kneighbors(X)
    # w^i_j, sigma, x^ in paper Robust Hessian LLE
    # w_outlier = w^i_j spanned in N*N
    w_outlier = np.zeros((N, N))
    sigmas = np.mean(distances[:, 1:], axis=1) ** 2
    x_knn_mean = np.mean(X[indices[:, 1:]], axis=1)
    checked = np.zeros(N, dtype=bool)
    loop = 0
    while loop <= max_iter:
        x_knn_mean_new = np.zeros(x_knn_mean.shape)
        # the denominator
        bot_sum = np.zeros(N)
        for i in range(N):
            for j in indices[i, 1:]:
                bot_sum[i] += np.exp(-np.linalg.norm(X[j] - x_knn_mean[i]) ** 2 / sigmas[i])
        # the numerator
        for i in range(N):
            # ignore already fitted sample
            if checked[i]: continue
            for j in indices[i, 1:]:
                w_outlier[i, j] = np.exp(-np.linalg.norm(X[j] - x_knn_mean[i]) ** 2 / sigmas[i]) / bot_sum[i]
                x_knn_mean_new[i] += w_outlier[i, j] * X[j]
            if np.linalg.norm(x_knn_mean_new[i] - x_knn_mean[i]) < tol:
                checked[i] = True
                continue
            x_knn_mean[i] = x_knn_mean_new[i]
        if np.all(checked):
            # print("identify loops:", loop)
            return w_outlier
        loop += 1
    # print("identify loops:", loop)
    return w_outlier #, x_knn_mean

def fast_od_step2(X):
    """
    TODO: how were the variables initialized
    :param X:
    :param w_outlier:
    :return:
    """
    N, n = X.shape
    pca = PCA()
    # U in Eq.14
    U, S, V = pca._fit(X)
    # projection error weight Eq.16, TODO:assume that initial projection error as following
    X_inv = pca.inverse_transform(pca.fit_transform(X))
    err = np.power(X_inv - X, 2)
    err_mean = np.mean(err, axis=1)
    err_weight = np.ones((N, n))
    for i in range(N):
        for j in range(n):
            if err[i, j] > err_mean[i]/2.0:
                err_weight = err_mean[i]/(err[i, j]*2)


def get_score_rhlle(X, k=None, tol=1e-2, max_iter=1000):
    w_outlier = fast_outlier_iden_step1(X, k=k, tol=tol, max_iter=max_iter)
    w_outlier_norm = w_outlier/np.sum(w_outlier, axis=1)
    score = -np.sum(w_outlier_norm, axis=0)
    return score

def pre_process_rhlle(X, color=None, alpha=0.2, tol=1e-2, max_iter=1000):
    """
    :param X: N*n, input data
    :param color: N dimensional array, input labels
    :param alpha: float, the threshold
    :param tol: float, parameter for the identifier algorithm
    :param max_iter: int, parameter for the identifier algorithm
    :return: data set with recognized outliers removed

    """
    color_rem = None
    score = get_score_rhlle(X, tol=tol, max_iter=max_iter)
    maxv = np.amax(score)
    minv = np.amin(score)
    threshold = maxv - (maxv - minv)*alpha
    outlier_indices = np.argwhere(score > threshold)
    X_rem = np.delete(X, outlier_indices, axis=0)
    if color is not None:
        color_rem = np.delete(color, outlier_indices, axis=0)
    return X_rem, color_rem