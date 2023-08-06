import numpy as np
from sklearn.datasets import *
from pyod.utils.data import generate_data
from sklearn.utils import check_random_state
from sklearn import preprocessing
from scipy.io import arff
import h5py
import scipy

def make_3d_helix(N=None, anomaly_rate=0.01, center=None, a=None, c=None, span=None):
    """

    :param N:
    :param anomaly_rate:
    :param center:
    :return:
    """
    if N is None: n = 1000
    else: n = N
    helix_dense = 0.05
    theta = np.linspace(0, 150, n)
    c, a = 3, 1
    x = (c + a * np.cos(theta)) * np.cos(theta * helix_dense)
    y = (c + a * np.cos(theta)) * np.sin(theta * helix_dense)
    z = a * np.sin(theta)

    X_helix = np.array([x, y, z]).T
    color_helix = theta
    return X_helix, color_helix

def make_2d_square(N=None, anomaly_rate=0.01, center=None):
    """
    rebuild the dataset in paper <manifold learning techniques for unsupervised anomaly detection>
    :param N: number of background points
    :param anomaly_rate:
    :param center:
    :return:
    """
    if center is None: center = np.array([1.5, 1.5])
    if N is None: N = 1000
    half_edge = 1.
    edge_num = int(N/4)
    outlier_num = int(N*anomaly_rate)

    l_edge = np.concatenate((np.random.uniform(center[0]-half_edge-0.1, center[0]-half_edge+0.1, edge_num).reshape((edge_num, 1)),
                             np.random.uniform(center[1]-half_edge+0.11, center[1]+half_edge+0.1, edge_num).reshape((edge_num, 1))),
                            axis=1)
    b_edge = np.concatenate((np.random.uniform(center[0] - half_edge - 0.1, center[0] + half_edge - 0.11, edge_num).reshape((edge_num, 1)),
                             np.random.uniform(center[1] - half_edge - 0.1, center[1] - half_edge + 0.1, edge_num).reshape((edge_num, 1))),
                            axis=1)
    r_edge = np.concatenate((np.random.uniform(center[0] + half_edge - 0.1, center[0] + half_edge + 0.1, edge_num).reshape((edge_num, 1)),
                             np.random.uniform(center[1] - half_edge - 0.1, center[1] + half_edge - 0.11, edge_num).reshape((edge_num, 1))),
                            axis=1)
    t_edge = np.concatenate((np.random.uniform(center[0] - half_edge + 0.11, center[0] + half_edge + 0.1, edge_num).reshape((edge_num, 1)),
                             np.random.uniform(center[1] + half_edge - 0.1, center[1] + half_edge + 0.1, edge_num).reshape((edge_num, 1))),
                            axis=1)
    X_in = np.concatenate((l_edge, b_edge, r_edge, t_edge), axis=0)
    color_in = np.zeros(X_in.shape[0])

    out2 = np.concatenate(
        (np.random.uniform(0, 3, outlier_num*10).reshape((outlier_num*10, 1)),
         np.random.uniform(0, 3, outlier_num*10).reshape((outlier_num*10, 1))),
        axis=1)
    X_out = out2[(((out2[:, 0]<center[0] - half_edge - 0.15) | (out2[:, 0]>center[0] + half_edge + 0.15) |
            (out2[:, 1]<center[1] - half_edge - 0.15) | (out2[:, 1]>center[1] + half_edge + 0.15)) |
                 ((out2[:, 0]>center[0] - half_edge + 0.15) & (out2[:, 0]<center[0] + half_edge - 0.15) &
                  (out2[:, 1]>center[1] - half_edge + 0.15) & (out2[:, 1]<center[1] + half_edge - 0.15)))]
    X_out = X_out[np.random.choice(range(X_out.shape[0]), size=outlier_num)]
    color_out = np.ones(X_out.shape[0])
    return np.concatenate((X_in, X_out), axis=0), np.concatenate((color_in, color_out), axis=0)

def make_2d_circle(N=1000, anomaly_rate=0.03, return_bg=False):
    X, _ = make_circles(N, noise=0.01, factor=0.99)
    offset = 1.1*np.max(X)
    n_outliers = int(N*anomaly_rate)
    random_state = check_random_state(None)
    outliers = random_state.uniform(low=-1. * offset, high=offset,
                                    size=(n_outliers, 2))
    X = np.concatenate((X, outliers), axis=0)
    color = np.zeros(N)
    color = np.concatenate((color, np.ones(n_outliers)), axis=0)
    X = X + np.array([1, 1])
    if return_bg:
        return X, color, X[:N], color[:N]
    return X, color

def get_hdf(f, num_sub_sample=700):
    data = h5py.File(f)
    X, color = data.items()
    X = np.c_[X[1][0], X[1][1], X[1][2]]
    color = color[1][0]
    temp_ind = np.argsort(color)
    X = X[temp_ind]
    color = color[temp_ind]
    N,_ = X.shape

    num_outlier = int(np.sum(color))
    num_sample = int(N - num_outlier)
    ind = np.argsort(color)
    color = color[ind]
    X = X[ind]
    if num_outlier > num_sub_sample * 0.05:
        num_outlier_new = int(num_sub_sample * 0.05)
        if num_sample > num_sub_sample:
            sub_ind = np.arange(0, num_sample, int(num_sample / num_sub_sample), dtype=int)  #
            X = np.concatenate((X[sub_ind], X[-num_outlier:-num_outlier_new]), axis=0)
            color = np.concatenate((color[sub_ind], color[-num_outlier:-num_outlier_new]), axis=0)
        else:
            X = np.concatenate((X[:num_sample], X[-num_outlier:-num_outlier_new]), axis=0)
            color = np.concatenate((color[:num_sample], color[-num_outlier:-num_outlier_new]), axis=0)
    X = preprocessing.normalize(X, norm='l2')
    return X, color

def get_mat(f, num_sub_sample=1000):
    data_wbc = scipy.io.loadmat(f)
    X = data_wbc['X'][:]
    N,_ = X.shape

    color = data_wbc['y'].flatten()
    num_outlier = np.sum(color)
    num_sample = int(N - num_outlier)
    ind = np.argsort(color)
    color = color[ind]
    X = X[ind]
    if num_outlier > num_sub_sample * 0.05:
        num_outlier = int(num_sub_sample * 0.05)
        if num_sample > num_sub_sample:
            sub_ind = np.arange(0, num_sample, int(num_sample / num_sub_sample), dtype=int)#
            X = np.concatenate((X[sub_ind], X[-num_outlier:]), axis=0)
            color = np.concatenate((color[sub_ind], color[-num_outlier:]), axis=0)
        else:
            X = np.concatenate((X[:num_sample], X[-num_outlier:]), axis=0)
            color = np.concatenate((color[:num_sample], color[-num_outlier:]), axis=0)
    X = preprocessing.normalize(X, norm='l2')
    return X, color

def get_arff(f, num_feature=None, num_sub_sample=1000):
    data, att = arff.loadarff(f)
    N = data.shape[0]
    num_outlier = 0
    X = np.zeros((N, num_feature))
    color = np.zeros((N,))
    for i in range(N):
        if data[i][num_feature+1].decode() == 'no':
            color[i] = 0
        else:
            num_outlier += 1
            color[i] = 1
        if num_feature>30:
            for j in range(10):
                X[i, j] = data[i][j]
        else:
            for j in range(num_feature):
                X[i, j] = data[i][j]
    num_sample = N - num_outlier
    ind = np.argsort(color)
    color = color[ind]
    X = X[ind]
    if num_sample > num_sub_sample:
        if num_outlier > num_sub_sample*0.05:
            num_outlier = int(num_sub_sample*0.05)
        sub_ind = np.arange(0, num_sample, int(num_sample / num_sub_sample), dtype=int)
        X = np.concatenate((X[sub_ind], X[-num_outlier:]), axis=0)
        color = np.concatenate((color[sub_ind], color[-num_outlier:]), axis=0)
    X = preprocessing.normalize(X, norm='l2')
    return X, color
def make_pyod_data(N=1000, n_features=2, anomaly_rate=0.1):
    """

    :param N: number of inliers
    :param n_features:
    :param anomaly_rate: outliers are int(N*anomaly_rate)
    :return:
    """
    X, labels = generate_data(n_train=N, n_features=n_features, contamination=anomaly_rate, train_only=True)
    return X, labels