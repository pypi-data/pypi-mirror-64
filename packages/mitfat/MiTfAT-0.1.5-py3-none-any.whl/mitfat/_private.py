#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 16:08:45 2020

@author: vbokharaie
"""

from mitfat import _Lib

__methods__ = []  # self is a DataStore
register_method = _Lib.register_method(__methods__)


# %%
@register_method
def cluster(self, X_train, num_clusters):
    """A wrapper for clustering mthoeds.
    calls cluster_scalar if input data is 1 dimentional,
    otherwise calls cluster_raw.

    Parameters
    ----------
    X_train: 'numpy.ndarray', (N=1, N_voxels)
    no_clusters: 'int'

    Returns
    -------
    cluster_labels_sorted: 'numpy.ndarray', (N_voxel, 1)
    cluster_centroids_sorted:'numpy.ndarray',

    See-also
    --------
    cluster_scalar, cluster_raw
    """
    
    from mitfat.clustering import cluster_scalar, cluster_raw
    print("X_train dimensions:", X_train.shape)
    # print("Number of voxels:", self.num_voxels)
    # print("Number of time steps:", self.num_time_steps)
    if X_train.shape[0] == 1 or len(X_train.shape) == 1:
        cluster_labels, cluster_centroid = cluster_scalar(X_train, num_clusters)
    elif X_train.shape[0] > 1 and X_train.shape[0] <= self.num_time_steps:
        cluster_labels, cluster_centroid = cluster_raw(X_train, num_clusters)
    else:
        import sys

        print(
            "Something wrong with the dimension of data while clustering:",
            sys.exc_info()[0],
        )
        raise
    return cluster_labels, cluster_centroid

# %%
@register_method
def cluster_hierarchial(self, signal="raw", num_clusters=2, if_save_plot=False):
    """Hieararchical clustering
    First 2 cluster over all data,
    choose all voxels corresponding to bigger centroid
    Then 2 clusters over these voxels.

    Parameters
    ----------
    signal: {'raw', 'mean', 'slope', 'slope'Segments', 'mean_segments'}
    num_clusters: int
        default=2
    if_save_plot: 'bool'
        default=False

    Returns
    -------
        cluster_labels2: 'list' of 'int'
        cluster_centroid2: 'numpy.ndarray'

    Notes
    -----
    Incomplete for 'mean', 'slope', 'slope'Segments', 'mean_segments'
    """
    import numpy as np
    from mitfat.clustering import cluster_raw
    
    if signal == "raw":
        x_train = self.data
        x_train_label = "RAW_hierarchical"
        cluster_labels, cluster_centroid = cluster_raw(x_train, num_clusters)
        ###
        mask_bbox = self.bbox_mask
        # hieararchical clustering
        target_cluster = 1  # biggest values in sorted clusters
        x_new = x_train[:, cluster_labels == target_cluster]
        self.data_hierarchical = x_new
        bbox_new_temp = np.int8(np.zeros(np.shape(mask_bbox))) - 1
        bbox_new = np.int8(np.zeros(np.shape(mask_bbox)))

        bbox_new_temp[mask_bbox == 1] = cluster_labels
        bbox_new[bbox_new_temp == target_cluster] = 1
        self.bbox_mask_hierarchical = bbox_new
        cluster_labels2, cluster_centroid2 = cluster_raw(x_new, num_clusters)

        if if_save_plot:
            self.save_clusters(x_new, x_train_label, cluster_labels2, cluster_centroid2)
            self.plot_clusters(
                x_new,
                x_train_label,
                cluster_labels2,
                cluster_centroid2,
                if_hierarchical=True,
            )

    return cluster_labels2, cluster_centroid2
