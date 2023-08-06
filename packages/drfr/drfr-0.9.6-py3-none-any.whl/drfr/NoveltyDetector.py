from sklearn.metrics.pairwise import rbf_kernel
import numpy as np
import scipy
from DiffusionMap import diff_map
from RobustHessianLLE import *
from sklearn.ensemble import RandomForestClassifier as rfc
from ripser import Rips
from sklearn.decomposition import PCA as PCA_dec
from pyod.models.pca import PCA
from pyod.models.ocsvm import OCSVM
from pyod.models.iforest import IForest
from pyod.models.lof import LOF

def compute_kij_slash(X, gamma=0.4):
    """
    compute the k_ij_slash matrix according to H.Hoffman Eq.4
    :param X: array-like (N,n)
    :argument
    :return k_ij_slash: array-like (N,N)
    """
    N,_ = X.shape
    k_ij_matrix = rbf_kernel(X, gamma=gamma)
    k_ir_vec = np.sum(k_ij_matrix, axis=0)/N
    k_rs = np.sum(k_ij_matrix, axis=None)/(N**2)
    k_ij_slash = np.zeros((N, N))
    # for i in range(N):
    #     for j in range(N):
    #         k_ij_slash[i, j] = k_ij_matrix[i, j] - k_ir_vec[i] - k_ir_vec[j] + k_rs
    i, j = np.meshgrid(k_ir_vec, k_ir_vec)
    k_ij_slash = k_ij_matrix - i - j + k_rs
    return k_ij_slash

# TODO: Fix
def compute_projection(X, current_x_id, alphas=None, k_ij_slash=None,
                       current_component=None):
    """
    compute the projection according to Eq.9 in Hoffman's paper.
    Projection: from hyper-high dimensional to n_component-dimensional, as potential
    :param X: (N,n)
    :param current_x_id: int
    :param current_component: int, ranged from 1 to n_principal_component
    :param alphas : array, row-eigenvectors
    :param k_ij_slash: array, K'ij matrix
    :argument
    :return projection: float, the error of current_x
    """
    N,_ = X.shape

    # main computation
    projection = 0
    for i in range(N):
        projection += alphas[current_component, i]*k_ij_slash[current_x_id, i]
    return projection

def compute_sphere_potential(X,gamma=None):
    """
    compute potential of data X[current_x] according to Eq.7 in Hoffman's paper. Larger cardinal means more anomaly
    :param X: (N,n)
    :return potentials: (N,)
    """
    N, _ = X.shape
    k_ij_matrix = rbf_kernel(X, gamma=gamma)
    potentials = -np.sum(k_ij_matrix, axis=0)*2./N
    return potentials


def pre_process_reduction(X, min_expl_var_ratio=95, method="pca", ReductionModel=None):
    """
    pre-process a data matrix to prevent singular covar-matirx
    :param X:
    :param n_principal_component:
    :param max_expl_var_ratio: float, percent of acceptable minimal explained variance ratio
    :param method: string, "pca" and other non linear reduction method tags
    :param ReductionModel, modul
    :return:
    """
    N, n = X.shape
    cov_matrix = PCA(n_components=n)
    cov_matrix.fit(X)
    var = np.cumsum(np.round(cov_matrix.explained_variance_ratio_, decimals=3) * 100)
    red_n_components = np.argwhere(var > min_expl_var_ratio)[0, 0] + 1

    if method != "pca":
        # non-linear dimension reduction
        red_model = ReductionModel.ReductionModel(n_neighbors=int(red_n_components*(red_n_components+3)/2)+1,
                                                  n_components=red_n_components)
        X_red = red_model.get_reduction(X, tag=method)
    else:
        X_red = PCA_dec(n_components=red_n_components).fit_transform(X)

    return X_red
def k_pca_evaluate(X, n_principal_component=20, gamma=0.6, min_expl_var_ratio=95):
    """

    :param X:
    :param n_principal_component: int, number of largest vectors we need
    :param gamma:
    :param max_expl_var_ratio: float, percent of acceptable minimal explained variance ratio
    :return:
    """
    N, _ = X.shape
    projections = np.zeros((N,))
    sphere_potential = compute_sphere_potential(X, gamma=gamma)
    k_ij_slash = compute_kij_slash(X, gamma=gamma)
    #if scipy.linalg.det(k_ij_slash) == 0:
    #    X = pre_process_reduction(X, min_expl_var_ratio=min_expl_var_ratio)
    # get greatest eigenvalues and vectors according to n_principal_component
    ## alphas == eigenvectors. used this name for consistence with paper
    eigenvalue, alphas = scipy.linalg.eigh(k_ij_slash)
    indices = eigenvalue.argsort()[-n_principal_component:][::-1]
    #eigenvalue = eigenvalue[indices]
    alphas = alphas[:, indices]
    for k in range(N):
        projection = 0
        for i in range(n_principal_component):
            projection += np.power(compute_projection(X, k, alphas=alphas.T, k_ij_slash=k_ij_slash,
                                                      current_component=i), 2)
        projections[k] = projection
    potentials = sphere_potential - projections
    scores = 1/np.absolute(potentials)
    return scores

def evaluate_novelty(X, labels=None, n_neighbors = None, n_principal_component=40, gamma=0.6, method="kpca",
                     npc_pca=2, sample_rate=0.15, time_step=1, alpha=1, background_num=None):
    """
    compute scores for all data in X. X with larger ABSOLUTE values are likely to be
    novelties. Support method: kpca, dmap, pca, lof, ocsvm, iforest, rforest, rbhessian.
    :param X: (N,n)
    :param n_principal_component: int, not larger than N
    :param gamma:
    :param alpha: float, [0, 1] to 0--density sensitive; to 1--geometry sensitive in diffusion map method
    :param pre_process: boolean
    :param min_expl_var_ratio: float, percent
    :param pre_process_method: string, "pca" and non linear reduction tags
    :param ReductionModel: modul
    :return scores: (N,)
    """
    ## make sample data for supervised learning
    N, _ = X.shape

    if labels is None:
        labels = np.zeros(N)
    if sample_rate > 1:
        print("invalid sample rate")
        return
    sample_size = int(N * sample_rate)
    #index = np.random.choice(N, sample_size, replace=False)
    #X_sampled = X[index]
    X_sampled = X[:sample_size]
    #labels_sampled = labels[index]
    labels_sampled = labels[:sample_size]
    if method == "kpca":
        scores = k_pca_evaluate(X, n_principal_component=n_principal_component, gamma=gamma)
    elif method == "dmap":
        dm = diff_map(X, gamma=gamma, sample_rate=sample_rate, time_step=time_step, alpha=alpha, background_num=background_num)
        scores = dm.diff_map_evaluate()
    elif method == "pca":
        od = PCA(n_components=npc_pca)
        od.fit(X)
        #scores = od.predict(X)
        scores = od.decision_scores_
    elif method == "lof":
        # Local Outlier Factor
        od = LOF(n_neighbors=n_neighbors)
        od.fit(X, labels)
        scores = od.decision_scores_
        #scores = od.predict(X)
    elif method == "ocsvm":
        od = OCSVM()
        od.fit(X, labels)
        scores = od.predict(X)
    elif method == "iforest":
        od = IForest()
        od.fit(X, labels)
        scores = od.predict(X)
    # classifiers as novelty detectors
    elif method == "rforest":
        clf = rfc(n_estimators=100, max_depth=2, random_state=0)
        clf.fit(X=X_sampled, y=labels_sampled)
        scores = -clf.predict_proba(X)[:, 0]
    # a fastoutlier det in rbhessian
    elif method == "rbhessian":
        scores = get_score_rhlle(X, k=n_neighbors)
    else:
        scores = k_pca_evaluate(X, n_principal_component=n_principal_component, gamma=gamma)
    return scores