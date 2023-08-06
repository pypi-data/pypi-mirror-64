from sklearn.metrics.pairwise import rbf_kernel
import numpy as np
import scipy
from scipy.sparse import linalg as splg
from sklearn import neighbors, preprocessing
from pyod.models.pca import PCA
import pydiffmap as dm
from scipy.special import softmax
# Begin Diffusion Map method
def compute_trans_matrix(X_S, alpha=0.9, gamma=0.8, time_step=None):
    N, _ = X_S.shape
    trans_matrix = np.zeros((N, N))
    #gamma = 1 / (2 * np.power(gamma, 2))
    misund = True
    kernel_S = rbf_kernel(X_S, gamma=gamma)
    if misund:
    # misunderstanding? when alpha==0, these two cases are equivalent
        for i in range(N):
            trans_matrix[i] = kernel_S[i]/\
                            (np.power(np.sum(kernel_S, axis=0), alpha)*
                            np.power(np.sum(kernel_S[i]), alpha))
            sum_temp = np.sum(trans_matrix[i])
            trans_matrix[i] /= sum_temp
    else:
        kernel = rbf_kernel(X_S, gamma=gamma)
        trans_matrix = kernel / np.sum(kernel, axis=0)
        trans_matrix = np.power(trans_matrix, time_step)

    # trans_matrix is not symmetric
    #print(np.allclose(trans_matrix.T, trans_matrix))
    return trans_matrix #trans_matrix

def make_diffusion_map(X_S, time_step=1, n_component=None, tol=1e-5, alpha=0.9, gamma=2):
    """
    make the diffusion map, aka diffusion coordinate matrix, given a whole dataset
    :param X:
    :return: eigenvalue, eigenvector, diffusion coordinate matrix, the diffusion map object
    """
    ### determine number of sustained eigs ###
    # sustain most explaining dimensions
    N, n = X_S.shape
    red_n = N - 1 # discard it
    ### end ###
    # for dimension reduction, irrelevant for od
    if n_component is not None and n_component <= N:
        red_n = n_component
    #clf = dm.diffusion_map.DiffusionMap.from_sklearn(alpha=alpha)
    #clf.fit(X_S)
    #trans_matrix = clf.L
    trans_matrix = compute_trans_matrix(X_S, alpha=alpha, gamma=gamma, time_step=time_step)
    #evals, evecs = splg.eigs(trans_matrix, k=red_n-1, which='LR')
    #ix = evals.argsort()[1:]
    evals, evecs = scipy.linalg.eigh(trans_matrix, eigvals=(N - red_n - 1, N - 1))
    ix = evals.argsort()[::-1][1:]

    eigenvalue = evals[ix].real
    #eigenvalue /= np.sum(eigenvalue)
    eigenvector = evecs[:, ix].real
    # for larger time step, discard vanishing eigenvalues
    for i in range(len(eigenvalue)):
        if eigenvalue[i]**time_step < tol:
            eigenvalue = eigenvalue[:i - 1]
            eigenvector = eigenvector[:, :i - 1]
            break
    if n_component is not None:
        eigenvector = preprocessing.normalize(eigenvector, norm='l2')
    diff_matrix = np.power(eigenvalue, time_step) * eigenvector
    #diff_matrix = np.power(-1./eigenvalue, time_step) * eigenvector
    return eigenvalue, eigenvector, diff_matrix

def compute_diffmap_kij_slash(X, y, gamma=0.4, alpha=0.5):
    """

    :param X: sample dataset
    :param y: out-of-sample
    :param gamma:
    :param alpha:
    :argument kij_slash_array: array of K'ij over j in {1,2,...,N}
    :return:
    """
    shape = X.shape
    """
    rbf_kernel([x, y], gamma=gamma)[0, 1]/\
               (np.power(np.sum(rbf_kernel(np.ones(shape)*x, X, gamma=gamma)[0]), alpha)*
                np.power(np.sum(rbf_kernel(np.ones(shape)*y, X, gamma=gamma)[0]), alpha))

    """
    # rbf_kernel(np.ones(shape)*y, X, gamma=gamma)[0]: array of [Kij] over y
    # rbf_kernel(X, gamma=gamma): part in q(x_i)
    # rbf_kernel needs matrix input, therefore expand y to X.shape
    kij_slash_array = rbf_kernel(np.ones(shape)*y, X, gamma=gamma)[0]/\
               (np.power(np.sum(rbf_kernel(X, gamma=gamma), axis=0), alpha)*
                np.power(np.sum(rbf_kernel(np.ones(shape)*y, X, gamma=gamma)[0]), alpha))
    return kij_slash_array


def compute_extension(X, y, eigenvalue, eigenvector, time_step=1, alpha=0.5, gamma=20):
    """

    :param X: sample dataset
    :param y: out-of-sample
    :param eigenvalue:
    :param eigenvector:
    :param time_step:
    :param alpha:
    :param gamma: float, controls the importance of difference of point coordinates
    :return:
    """
    #M = eigenvalue.shape[0]
    #N, _ = X.shape
    X_Sx = np.concatenate(([y], X), axis=0)
    sx_kernel = rbf_kernel(X_Sx, gamma=gamma)
    k_slash = sx_kernel[0] / \
              (np.power(np.sum(sx_kernel, axis=0), alpha) *
               np.power(np.sum(sx_kernel[0]), alpha))
    sum_k_slash = np.sum(k_slash)
    k_d = k_slash/sum_k_slash
    # ignore k(y, y)
    k_d = k_d[1:]
    sum_temp = k_d @ eigenvector
    #sum_check = np.zeros(M)
    #
    #for k in range(M):
    #    sum_check[k] = np.dot(eigenvector[:, k], k_d)
    diff_coord = sum_temp * np.power(eigenvalue, time_step)
    return diff_coord

def compute_nbors(diff_y, diff_matrix, k):
    combined = np.concatenate(([diff_y], diff_matrix), axis=0)
    nbors = neighbors.kneighbors_graph(X=combined, mode='distance', n_neighbors=k)
    inds = None
    # compute score
    for i, nbor_row in enumerate(nbors):
        inds = nbor_row.indices - 1
        break
    return inds

class diff_map():
    def __init__(self, X, gamma=2, extension_gamma=20, sample_rate=0.15, time_step=1, alpha=1, n_component=None, k=10, background_num=None):
        """

        :param X:
        :param gamma:
        :param sample_rate:
        :param k: int, neighbors
        :param time_step:
        :param background_num: int, X[: background_num] are treated as background
        :param alpha: float, controls dependency of the embedding to geometry and density. 0 to both, 1 to geometry only
        """
        N, n = X.shape
        # sample the background ONLY
        if background_num is None: background_num = int(N/1.2)
        self.sample_size = int(background_num * sample_rate)
        self.index = np.arange(0, background_num, int(background_num / self.sample_size), dtype=int)
        self.k = min(k, self.sample_size - 3)
        self.X = X
        self.X_out = self.X[background_num:]
        #index = np.random.choice(N, self.sample_size, replace=False)
        self.X_S = X[self.index]
        #print("sample index: ", self.index)
        #self.X_S = X[:int(N * sample_rate)]
        self.eigenvalue, self.eigenvector, self.diff_matrix= \
            make_diffusion_map(self.X_S, time_step=time_step, n_component=n_component, alpha=alpha, gamma=gamma)
        self.gamma = gamma
        self.extension_gamma = extension_gamma
        self.time_step = time_step
        self.alpha = alpha
        self.pydiffmapclf = dm.diffusion_map.DiffusionMap.from_sklearn(k=self.k, n_evecs=1+self.diff_matrix.shape[1], alpha=alpha)
        self.num_bg = 0

    def get_diffusion_space(self):
        N, n = self.X.shape
        diff_space = np.ones((N, self.diff_matrix.shape[1]))
        j = 0
        for i in range(N):
            if i in self.index:
                diff_space[i] = self.diff_matrix[j]
                j += 1
                # self.num_bg += 1
            else:
                diff_space[i] = compute_extension(self.X_S, self.X[i], self.eigenvalue, self.eigenvector,
                                                  time_step=self.time_step, alpha=self.alpha, gamma=self.extension_gamma)
            i += 1
        return diff_space

    def diff_map_evaluate(self, return_index=False):
        """
        Evaluate dataset
        :param k:
        :return:
        """
        N, n = self.X.shape
        scores = np.ones(N)
        for i in range(N):
            if i in self.index:
                scores[i] = 0
                #self.num_bg += 1
            else:
                scores[i] = self.diff_map_evaluate_single(self.X[i])
            i += 1
        if not return_index:
            return scores
        return scores, self.index

    def get_neighbor(self, y=None):
        if y is None:
            outlier_nbors = np.zeros((self.X_out.shape[0], self.k))
            j = 0
            for x in self.X_out:
                diff_x = compute_extension(self.X_S, x, self.eigenvalue, self.eigenvector,
                                           time_step=self.time_step, alpha=self.alpha, gamma=self.gamma)
                outlier_nbors[j] = compute_nbors(diff_x, self.diff_matrix, self.k)
                j += 1
        else:
            diff_y = compute_extension(self.X_S, y, self.eigenvalue, self.eigenvector,
                                       time_step=self.time_step, alpha=self.alpha, gamma=self.gamma)
            outlier_nbors = compute_nbors(diff_y, self.diff_matrix, self.k)
        return outlier_nbors

    def get_neighborhood_color(self):
        """

        :return: the density of neighborhood reference, in form of array, corresponding to sampled data X_S
        """
        _, M = self.diff_matrix.shape
        nbor_color = np.zeros(self.X_S.shape[0])
        # compute diffusion coordinate
        ## treat background as non-ouliers
        for y in self.X:
            if y in self.X_S:
                continue
            diff_y = compute_extension(self.X_S, y, self.eigenvalue, self.eigenvector,
                                   time_step=self.time_step, alpha=self.alpha, gamma=self.extension_gamma)
            combined = np.concatenate(([diff_y], self.diff_matrix), axis=0)
            nbors = neighbors.kneighbors_graph(X=combined, mode='distance', n_neighbors=self.k)
            # compute score
            for i, nbor_row in enumerate(nbors):
                inds = nbor_row.indices - 1
                nbor_color[inds] += 1
                break
        return nbor_color, self.X_S

    def diff_map_evaluate_pydiffmap(self):
        """
        use pydiffmap to calculate skeleton diffusion and out-of-sample
        :return:
        """
        self.diff_matrix_pydm = self.pydiffmapclf.fit_transform(self.X_S)
        M = self.diff_matrix_pydm.shape[1]
        centroid = np.zeros(M)
        covk_matrix = np.zeros((M, M))
        scores = np.ones(self.X.shape[0])
        Y = self.pydiffmapclf.transform(self.X)
        j = 0
        for y in Y:
            if j < self.index.shape[0]:
                scores[j] = 0
                j += 1
                continue
            combined = np.concatenate(([y], self.diff_matrix_pydm), axis=0)
            nbors = neighbors.kneighbors_graph(X=combined, mode='distance', n_neighbors=self.k)
            # compute score
            for i, nbor_row in enumerate(nbors):
                inds = nbor_row.indices
                centroid = np.sum(combined[inds], axis=0) / self.k
                for x in combined[inds]:
                    covk_matrix += np.outer(x - centroid, x - centroid)
                break
            _, unit_normal = scipy.linalg.eigh(covk_matrix, eigvals=(0, 0))
            # print("eigenvalues: ", scipy.linalg.eigh(covk_matrix), scipy.linalg.eigh(covk_matrix, eigvals=(0, 0)))
            unit_normal = unit_normal[:, 0]
            scores[j] = (y - centroid) @ unit_normal
            j += 1
        return scores, self.index

    def diff_map_evaluate_single(self, y):
        """
        Evaluate one sample
        :param y:
        :param k:
        :return: score of current evaluate, greater means more likely outlier
        """
        _, M = self.diff_matrix.shape
        centroid = np.zeros(M)
        covk_matrix = np.zeros((M, M))
        # compute diffusion coordinate
        ### treat background as inliers
        # if y in self.X_S:
        #     self.num_bg += 1
        #     return 0
        diff_y = compute_extension(self.X_S, y, self.eigenvalue, self.eigenvector,
                                   time_step=self.time_step, alpha=self.alpha, gamma=self.extension_gamma)
        combined = np.concatenate(([diff_y], self.diff_matrix), axis=0)
        nbors = neighbors.kneighbors_graph(X=combined, mode='distance', n_neighbors=self.k)
        # compute score
        for i, nbor_row in enumerate(nbors):
            inds = nbor_row.indices
            centroid = np.sum(combined[inds], axis=0) / self.k
            for x in combined[inds]:
                covk_matrix += np.outer(x - centroid, x - centroid)
            break
        #print("covk_matrix det and is_symm: ", scipy.linalg.det(covk_matrix), np.allclose(covk_matrix, covk_matrix.T))
        _, unit_normal = scipy.linalg.eigh(covk_matrix, eigvals=(0, 0))
        #print("eigenvalues: ", scipy.linalg.eigh(covk_matrix), scipy.linalg.eigh(covk_matrix, eigvals=(0, 0)))
        unit_normal = unit_normal[:, 0]
        score = np.absolute((diff_y - centroid) @ unit_normal)
        return score

# End Diffusion Map method